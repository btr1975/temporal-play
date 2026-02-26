"""
Nexus Worker creator
"""

from typing import Sequence, Any
import logging

from temporalio.client import Client
from temporalio.worker import Worker


def get_nexus_worker(
    client: Client, task_queue: str, workflows: Sequence[type], nexus_service_handlers: Sequence[Any]
) -> Worker:
    """Get a Nexus worker

    :param client: Nexus client
    :param task_queue: Nexus task queue
    :param workflows: Nexus workflows
    :param nexus_service_handlers: Nexus service handlers

    :return: Nexus worker
    """
    logging.basicConfig(level=logging.INFO)
    print("Starting Nexus Worker")
    worker = Worker(
        client=client,
        task_queue=task_queue,
        workflows=workflows,
        nexus_service_handlers=nexus_service_handlers,
    )

    return worker
