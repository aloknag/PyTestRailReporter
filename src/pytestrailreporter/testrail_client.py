# src/pytestrailreporter/testrail_client.py
"""Module for configuring the TestRail client."""

import logging

import pytest
from tenacity import retry, stop_after_attempt, wait_exponential
from testrail_api import TestRailAPI


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, max=10))
def configure_testrail_client(url, user, password):
    """
    Configures TestRail API client with retries.

    :param url: TestRail URL.
    :param user: TestRail user.
    :param password: TestRail password.

    :return: TestRail API client.
    """
    try:
        client = TestRailAPI(url, user, password)
        return client
    except Exception as e:
        logging.error("Error configuring TestRail client: %s", e)
        raise pytest.UsageError(f"Error configuring TestRail client: {e}")


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, max=10))
def add_testrail_run(client, project_id, run_name):
    """
    Creates a new TestRail run with retries.

    :param client: TestRail API client.
    :param project_id: TestRail project ID.
    :param run_name: TestRail run name.

    :return: TestRail run ID.
    """
    try:
        run_id = client.runs.add_run(project_id=project_id, name=run_name, include_all=True)["id"]
        return run_id
    except Exception as e:
        logging.error("Error creating TestRail run: %s", e)
        raise


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, max=10))
def add_testrail_result_for_case(client, run_id, case_id, status_id, comment):
    """
    Adds a test result for a specific case with retries.

    :param client: TestRail API client.
    :param run_id: TestRail run ID.
    :param case_id: TestRail case ID
    :param status_id: TestRail status ID.
    :param comment: TestRail comment.

    :return: None
    """
    try:
        client.results.add_result_for_case(run_id=run_id, case_id=case_id, status_id=status_id, comment=comment)
    except Exception as e:
        logging.error("Error adding TestRail result: %s", e)
        raise
