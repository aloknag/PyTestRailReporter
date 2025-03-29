# src/pytestrailreporter/plugin.py
"""Pytest plugin for TestRail integration."""

import logging
import os
import threading

import pytest

from .config import load_config, validate_config
from .result_sender import result_queue, send_testrail_results
from .testrail_client import add_testrail_run, configure_testrail_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def pytest_addoption(parser):
    """Add options to configure TestRail integration.

    :param parser:  The pytest argument parser.
    """
    group = parser.getgroup("testrail", "TestRail integration")
    group.addoption(
        "--testrail-url",
        action="store",
        help="TestRail URL",
        default=os.environ.get("TESTRAIL_URL"),
    )
    group.addoption(
        "--testrail-user",
        action="store",
        help="TestRail user",
        default=os.environ.get("TESTRAIL_USER"),
    )
    group.addoption(
        "--testrail-password",
        action="store",
        help="TestRail password",
        default=os.environ.get("TESTRAIL_PASSWORD"),
    )
    group.addoption(
        "--testrail-project-id",
        type=int,
        help="TestRail project ID",
        default=os.environ.get("TESTRAIL_PROJECT_ID"),
    )
    group.addoption(
        "--testrail-run-name",
        help="TestRail run name",
        default=os.environ.get("TESTRAIL_RUN_NAME"),
    )
    group.addoption("--testrail-config", help="Path to TestRail config YAML")


def pytest_configure(config):
    """Configure TestRail integration.

    :param config: The pytest config object.
    """
    config.addinivalue_line("markers", "testrail_cases(cases): Mark test with TestRail case IDs.")
    config.testrail_client = None
    config.testrail_run_id = None
    try:
        testrail_config = load_config(config)
        validate_config(testrail_config)
        config.testrail_client = configure_testrail_client(
            testrail_config["url"],
            testrail_config["user"],
            testrail_config.get("password"),
        )
        config.testrail_run_id = add_testrail_run(
            config.testrail_client,
            testrail_config["project_id"],
            testrail_config["run_name"],
        )
        logging.info("TestRail run created: %s", config.testrail_run_id)
        threading.Thread(
            target=send_testrail_results,
            args=(config.testrail_client, config.testrail_run_id),
            daemon=True,
        ).start()
    except Exception as e:  # pylint: disable=broad-exception-caught
        pytest.exit(f"Failed to configure TestRail: {e}")


def pytest_runtest_makereport(item, call):
    """Capture test results and TestRail case IDs.

    :param item:  The pytest test item object.
    :param call:  The pytest call object.
    """
    if hasattr(item, "testrail_cases"):
        cases = item.testrail_cases
        status = None
        comment = ""
        if call.when == "call":
            if call.excinfo is None:
                status = 1  # Passed
            else:
                if isinstance(call.excinfo.value, AssertionError):
                    status = 5  # Failed
                else:
                    status = 4  # Blocked, or other error.
                comment = str(call.excinfo.value)
            if hasattr(item, "testrail_comments"):
                comment += "\n" + item.testrail_comments
            for case_id in cases:
                if item.config.testrail_run_id:
                    result_queue.put(
                        {
                            "case_id": int(case_id.replace("C", "")),
                            "status_id": status,
                            "comment": comment,
                        }
                    )


def pytest_collection_modifyitems(items):
    """Add TestRail case IDs to test items.

    :param items:  List of pytest test items.
    """
    for item in items:
        marker = item.get_closest_marker("testrail_cases")
        if marker:
            item.testrail_cases = marker.args[0]
            item.testrail_comments = ""


def pytest_runtest_setup(item):
    """Allows to add comments to the test item.

    :param item: The pytest test item
    """

    def add_testrail_comment(comment):
        item.testrail_comments += comment + "\n"

    item.add_testrail_comment = add_testrail_comment


def pytest_sessionfinish():
    """Signal the result sender thread to stop."""
    result_queue.join()
    result_queue.put(None)
    logging.info("TestRail result sender thread stopped.")
