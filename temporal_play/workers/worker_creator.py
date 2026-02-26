"""
Worker creator
"""

from typing import Sequence, Any
import inspect
from concurrent.futures import ThreadPoolExecutor
import logging

from temporalio.client import Client
from temporalio.worker import Worker


def get_worker(client: Client, task_queue: str, workflows: Sequence[type], activities: Sequence[Any]) -> Worker:
    """Get a Worker instance

    :param client: Client object
    :type client: Client
    :param task_queue: Task queue name
    :type task_queue: str
    :param workflows: Workflow list
    :type workflows: Sequence[type]
    :param activities: Activity list
    :type activities: Sequence[Any]

    :rtype: Worker
    :returns: A Worker instance
    """
    logging.basicConfig(level=logging.INFO)
    if all(inspect.iscoroutinefunction(activity) for activity in activities):
        print("Using Async Worker")
        worker = Worker(
            client=client,
            task_queue=task_queue,
            workflows=workflows,
            activities=activities,
        )

    else:
        print("Using ThreadPoolExecutor Worker")
        worker = Worker(
            client=client,
            task_queue=task_queue,
            workflows=workflows,
            activities=activities,
            activity_executor=ThreadPoolExecutor(max_workers=50),
        )

    return worker
