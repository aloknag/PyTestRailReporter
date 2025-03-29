# src/pytestrailreporter/result_sender.py
import queue
import threading
import logging
from .testrail_client import add_testrail_result_for_case

result_queue = queue.Queue()

def send_testrail_results(testrail_client, run_id):
    """Worker thread to send TestRail results asynchronously."""
    while True:
        result = result_queue.get()
        if result is None:
            break
        try:
            add_testrail_result_for_case(
                testrail_client, run_id, result['case_id'], result['status_id'], result['comment']
            )
            logging.info(f"TestRail result sent: Case {result['case_id']}")
        except Exception as e:
            logging.error(f"Error sending TestRail result: Case {result['case_id']}: {e}")
        result_queue.task_done()