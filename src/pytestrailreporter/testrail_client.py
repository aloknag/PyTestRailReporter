# src/pytestrailreporter/testrail_client.py
from testrail_api import TestRailAPI
import logging
import pytest
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, max=10))
def configure_testrail_client(url, user, password):
    """Configures TestRail API client with retries."""
    try:
        client = TestRailAPI(url, user, password)
        return client
    except Exception as e:
        logging.error(f"Error configuring TestRail client: {e}")
        raise pytest.UsageError(f"Error configuring TestRail client: {e}")

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, max=10))
def add_testrail_run(client, project_id, run_name):
    """Creates a new TestRail run with retries."""
    try:
        run_id = client.runs.add_run(project_id=project_id, name=run_name, include_all=True)["id"]
        return run_id
    except Exception as e:
        logging.error(f"Error creating TestRail run: {e}")
        raise

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, max=10))
def add_testrail_result_for_case(client, run_id, case_id, status_id, comment):
    """Adds a test result for a specific case with retries."""
    try:
        client.results.add_result_for_case(
            run_id=run_id, case_id=case_id, status_id=status_id, comment=comment
        )
    except Exception as e:
        logging.error(f"Error adding TestRail result: {e}")
        raise