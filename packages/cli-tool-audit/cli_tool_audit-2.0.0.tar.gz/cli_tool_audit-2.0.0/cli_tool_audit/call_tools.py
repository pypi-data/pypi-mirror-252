"""
Check if an external tool is expected and available on the PATH.

Also, check version.

Possible things that could happen
- found/not found on path
- found but can't run without error
- found, runs but wrong version switch
- found, has version but cli version != package version
"""

import datetime
import logging
import os
import subprocess  # nosec
from typing import Optional

# pylint: disable=no-name-in-module
from whichcraft import which

from cli_tool_audit.known_switches import KNOWN_SWITCHES
from cli_tool_audit.models import SchemaType, ToolAvailabilityResult

logger = logging.getLogger(__name__)


def get_command_last_modified_date(tool_name: str) -> Optional[datetime.datetime]:
    """
    Get the last modified date of a command's executable.
    Args:
        tool_name (str): The name of the command.

    Returns:
        Optional[datetime.datetime]: The last modified date of the command's executable.
    """
    # Find the path of the command's executable
    result = which(tool_name)
    if result is None:
        return None

    executable_path = result

    # Get the last modified time of the executable
    last_modified_timestamp = os.path.getmtime(executable_path)
    return datetime.datetime.fromtimestamp(last_modified_timestamp)


def check_tool_availability(
    tool_name: str,
    schema: SchemaType,
    version_switch: str = "--version",
) -> ToolAvailabilityResult:
    """
    Check if a tool is available in the system's PATH and if possible, determine a version number.

    Args:
        tool_name (str): The name of the tool to check.
        schema (SchemaType): The schema to use for the version.
        version_switch (str): The switch to get the tool version. Defaults to '--version'.


    Returns:
        ToolAvailabilityResult: An object containing the availability and version of the tool.
    """
    # Check if the tool is in the system's PATH
    is_broken = True

    last_modified = get_command_last_modified_date(tool_name)
    if not last_modified:
        logger.warning(f"{tool_name} is not on path.")
        return ToolAvailabilityResult(False, True, None, last_modified)
    if schema == SchemaType.EXISTENCE:
        logger.debug(f"{tool_name} exists, but not checking for version.")
        return ToolAvailabilityResult(True, False, None, last_modified)

    if version_switch is None or version_switch == "--version":
        # override default.
        # Could be a problem if KNOWN_SWITCHES was ever wrong.
        version_switch = KNOWN_SWITCHES.get(tool_name, "--version")

    version = None

    # pylint: disable=broad-exception-caught
    try:
        command = [tool_name, version_switch]
        result = subprocess.run(command, capture_output=True, text=True, timeout=15, shell=False, check=True)  # nosec
        # Sometimes version is on line 2 or later.
        version = result.stdout.strip()
        if not version:
            # check stderror
            logger.debug("Got nothing from stdout, checking stderror")
            version = result.stderr.strip()

        logger.debug(f"Called tool with {' '.join(command)}, got  {version}")
        is_broken = False
    except subprocess.CalledProcessError as exception:
        is_broken = True
        logger.error(f"{tool_name} failed invocation with {exception}")
        logger.error(f"{tool_name} stderr: {exception.stderr}")
        logger.error(f"{tool_name} stdout: {exception.stdout}")
    except FileNotFoundError:
        logger.error(f"{tool_name} is not on path.")
        return ToolAvailabilityResult(False, True, None, last_modified)

    return ToolAvailabilityResult(True, is_broken, version, last_modified)


if __name__ == "__main__":
    print(get_command_last_modified_date("asdfpipx"))
    # check_tool_availability("isort")
    #
    # def run() -> None:
    #     """Example"""
    #     # Example usage
    #     file_path = "../pyproject.toml"
    #     cli_tools = read_config(file_path)
    #
    #     for tool, config in cli_tools.items():
    #         result = check_tool_availability(tool, config.version_switch or "--version")
    #         print(
    #             f"{tool}: {'Available' if result.is_available else 'Not Available'}"
    #             f" - Version:\n{result.version if result.version else 'N/A'}"
    #         )
    #
    # run()
