"""
The Main program to commit the palo alto resources.

:author: Johan Lanzrein
:file: commit.py
"""
import difflib
import logging
import time
from multiprocessing.pool import ThreadPool as Pool

import requests
import xmltodict
from nagra_panorama_api import Panorama
from nagra_panorama_api.restapi import PanoramaClient
from nagra_panorama_api.xmlapi import XMLApi, etree_tostring

log = logging.getLogger(__name__)


def api_call_status(response_dict: dict) -> str:
    """
    Get the api status.

    :param response_dict: the response from an XML api call
    :return: success or error
    """
    status = response_dict["response"]["@status"]
    if status in ("error", "success"):
        return status
    return None


def _push(
    url,
    api_key,
    devicegroup=None,
    description=None,
) -> bool:
    """
    Commit all operation to the given device groups.

    :param device: The device to commit to
    :return: True if an error occured, False otherwise
    """
    if devicegroup:
        log.info(f"Starting to push on devicegroup '{devicegroup}'...")
    else:
        log.info("Starting to push everything...")
    pano = Panorama(url, api_key=api_key)

    start = time.perf_counter()
    # Commit and wait if you don't want to wait and just fire and forget you can set sync and sync_all to false.
    # it's harder to see if there is any failures if you do that though.
    try:
        # Nb: commit-all is really the command that does the push
        # https://docs.paloaltonetworks.com/pan-os/10-2/pan-os-panorama-api/pan-os-xml-api-request-types/commit-configuration-api/commit-all
        result = pano.commit_all(
            sync=True,
            sync_all=True,
            exception=True,
            devicegroup=devicegroup,
            description=description,
        )
        log.info(
            "Got answer for commit at {} : Success {} ; result : {}".format(
                devicegroup,
                result["success"],
                result["result"],
            ),
        )
        message = "".join(result["messages"])
        if message:
            log.info(f"""Got following messages:\n{message}""")
        log.info(
            f"""Push on devicegroup '{devicegroup}' done in {int(round(time.perf_counter() - start))} seconds"""
        )
        return False
    except Exception as e:
        if devicegroup:
            log.error(f"Got error while trying to push on device '{devicegroup}': {e} ")
        else:
            log.error(f"Got error while trying to push on all devices: {e} ")
    log.info(
        f"""Push on devicegroup '{devicegroup}' done in {int(round(time.perf_counter() - start))} seconds"""
    )
    return True


def commit(
    url,
    api_key,
    admin: str,
    description="Terraform pipeline auto commit",
    verify=False,
    timeout=None,
) -> str:
    """
    Commit on the panorama
    :param admin: admin name under which to commit
    :param commit_type: the type of commit
    :return: error, fail, success, unchanged or timeout
    """
    api = XMLApi(url, api_key, verify=verify)
    # Check if there are changes pending to commit
    res = api.pending_changes().xpath(".//result/text()")[0]
    if res == "no":
        log.info("No change to commit")
        return "unchanged"
    description_tag = f"<description>{description}</description>"
    cmd = (
        "<commit><partial>"
        "<device-and-network>excluded</device-and-network>"
        "<shared-object>excluded</shared-object>"
        f"<admin><member>{admin}</member></admin>"
        f"{description_tag}"
        "</partial></commit>"
    )
    # Use this value instead to debug the job result check
    # cmd = "<commit></commit>"

    # Send request to commit and parse response into dictionary
    try:
        res = api._commit_request(cmd)  # noqa
        commit_response = xmltodict.parse(etree_tostring(res))["response"]
        # Commit sent successfully
        line = commit_response["result"]["msg"]["line"]
        log.info(
            f"""Success: {line}""",
        )
        job_id = commit_response["result"]["job"]
    except Exception as e:
        log.warning(e)
        if "No edits" in str(e):
            return "unchanged"
        return "error"
    try:
        delta_seconds = 20
        max_retry = 15
        # Loop to check the job status every 20 seconds until the job
        # is completed, or up to 5 minutes (15 retries)
        for _ in range(max_retry):
            log.info(f"Job pending - waiting {delta_seconds} seconds to check status")
            time.sleep(delta_seconds)
            # Send request and parse response in a dictionary
            job = api.get_jobs(job_id).xpath(".//job")
            if not job:
                log.error(f"Job with ID {job_id} does not exist")
            job = xmltodict.parse(etree_tostring(job[0]))["job"]

            result = job["result"]
            # If job is still pending, continue loop
            if result == "PEND":
                job_progress = job["progress"]
                log.info(
                    f"Job pending: {job_progress}% completed",
                )
                continue
            details = job["details"]
            details = details.get("line", "") if details else ""
            if isinstance(details, list):
                details = details[0]
            if result == "OK":
                log.info(f"Commit SUCCEED: {details}")
                return "success"
            if result == "FAIL":
                log.error(f"Commit FAILED: {details}")
                return "fail"
            log.error(f"ERROR: Received unexpected result '{result}'")
            return "error"
        log.warning(
            f"Commit pending for {delta_seconds * max_retry // 60} minutes - stopping script"
        )
        return "timeout"
    except Exception as e:
        log.error(f"Error while waiting for job completion: {e}")
        return "unchanged"


def check_pending_on_devices(
    devices: list,
    api_key,
    url,
    verify=False,
    timeout=None,
) -> bool:
    """
    Check if there is any pending changes specifically on a list of devices.

    :param devices: The devices to look up for
    :return: True if there are any pending changes.
    """
    api = XMLApi(url, api_key, verify=verify)
    result = api.uncommited_changes_summary()
    members = result.xpath(".//member/text()")
    if not members:
        return False
    if "DG1_GLOBAL" in devices:  # here DG1_GLOBAL == "any"
        return True
    return set(devices) & set(members)


def check_pending(url, api_key, verify=False, timeout=None) -> str:
    """
    Function to check if there are pending changes
    :return: "success" if changes are pending, return "error" if no changes
    """

    # Build URL
    api = XMLApi(url, api_key, verify=verify)
    pending = api.pending_changes().xpath("response/result/text()")
    return {
        "no": "error",
        "yes": "success",
    }.get(pending)


def config_diff(url, api_key, verify=False, timeout=None) -> str:
    """
    Function to compare candidate and running configurations

    :return: error string
    """
    if check_pending(url, api_key) == "error":
        log.info("No pending changes")
        return "error"

    api = XMLApi(url, api_key, verify=verify)
    # Send request for Candidate config, put response in a file
    candidate = etree_tostring(api.candidate_config())
    running = etree_tostring(api.running_config())

    # Running diff on the two files
    diff = difflib.context_diff(
        running.splitlines(),
        candidate.splitlines(),
        fromfile="Running",
        tofile="Candidate",
        n=3,
    )
    log.info("".join(list(diff)))
    return None


def revert_config(url, api_key, admin, verify=False, timeout=None) -> str:
    """
    Function to revert the pending changes (back to the running configuration)

    :param admin: The admin name under which to revert.
    """
    if check_pending(url, api_key) == "error":
        log.info("No change to revert")
        return "error"

    # Payload to revert
    payload_revert = {
        "type": "op",
        "key": api_key,
        "cmd": f"<revert><config><partial><admin><member>{admin}</member></admin></partial></config></revert>",
    }
    # Send request and put output in a dictionary
    response = requests.get(url, params=payload_revert, verify=verify, timeout=timeout)
    contents = xmltodict.parse(response.text)
    if api_call_status(contents) == "success":
        result = contents["response"]["result"]
        log.info(
            f"SUCCESS: {result}",
        )
        return None
    if api_call_status(contents) == "error":
        log.error(f"Could not revert the config : {contents}")
        return None
    return None


def get_all_device_groups(url, api_key) -> list:
    """
    Function to get all devices registered in Panorama
    """
    client = PanoramaClient(url, api_key)
    return [g["@name"] for g in client.panorama.DeviceGroups.get()]


def push(url, api_key, devicegroups, description=None, branch=None, commit_sha=None):
    if not devicegroups:
        log.warning("No devicegroup to push to")
    if "DG1_GLOBAL" in devicegroups:
        devicegroups = get_all_device_groups(url, api_key)
    # Sort the devices groups: this will help troubleshooting
    devicegroups = sorted(devicegroups)

    if not description:
        if branch and commit_sha:
            description = (
                f"Palo Alto pipeline update from {branch} (Commit Sha {commit_sha})"
            )
        else:
            description = "Automatic Palo Alto pipeline update"
    log.info(f"Number of firewalls to push to: {len(devicegroups)}")
    log.debug("\n".join(devicegroups))

    with Pool(len(devicegroups)) as pool:
        results = pool.map(
            lambda d: _push(url, api_key, d, description=description), devicegroups
        )
    error = any(results)
    if error:
        log.error("Push has failed on one or more Firewall")
    return error
