# src/pytestrailreporter/result_sender.py
"""Module for sending test results to TestRail."""

import logging
import queue
import threading  # pylint: disable=unused-import

from .testrail_client import add_testrail_result_for_case

result_queue = queue.Queue()


def send_testrail_results(testrail_client, run_id):
    """
    Worker thread to send TestRail results asynchronously.

    :param testrail_client: TestRail API client.
    :param run_id: TestRail run ID.

    :return: None
    """
    while True:
        result = result_queue.get()
        if result is None:
            break
        try:
            add_testrail_result_for_case(
                testrail_client,
                run_id,
                result["case_id"],
                result["status_id"],
                result["comment"],
            )
            logging.info("TestRail result sent: Case %s", result["case_id"])
        except Exception as e:  # pylint: disable=broad-except
            logging.exception("Error sending TestRail result: Case %s", result["case_id"], exc_info=e)
        result_queue.task_done()
    logging.info("TestRail result sender thread stopped.")
