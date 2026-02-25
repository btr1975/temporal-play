"""
Worker 1
"""

import asyncio
import inspect
from concurrent.futures import ThreadPoolExecutor

from temporalio.client import Client
from temporalio.worker import Worker

from temporal_play.activities.activities import ALL_ACTIVITIES
from temporal_play.workflows.workflows import ALL_WORKFLOWS


def get_worker(client: Client, task_queue: str) -> Worker:
    """Get a Worker instance

    :param client: Client object
    :type client: Client
    :param task_queue: Task queue name
    :type task_queue: str

    :rtype: Worker
    :returns: A Worker instance
    """
    if all(inspect.iscoroutinefunction(activity) for activity in ALL_ACTIVITIES):
        print("Using Async Worker")
        worker = Worker(
            client=client,
            task_queue=task_queue,
            workflows=ALL_WORKFLOWS,
            activities=ALL_ACTIVITIES,
        )

    else:
        print("Using ThreadPoolExecutor Worker")
        worker = Worker(
            client=client,
            task_queue=task_queue,
            workflows=ALL_WORKFLOWS,
            activities=ALL_ACTIVITIES,
            activity_executor=ThreadPoolExecutor(max_workers=50),
        )

    return worker


async def main(host: str, port: int, task_queue: str, namespace: str) -> None:
    """Main function

    :param host: Host IP address
    :type host: str
    :param port: Port number
    :type port: int
    :param task_queue: Task queue name
    :type task_queue: str
    :param namespace: Worker namespace
    :type namespace: str

    :rtype: None
    :returns: Nothing
    """
    client = await Client.connect(target_host=f"{host}:{port}", namespace=namespace)
    worker = get_worker(client=client, task_queue=task_queue)
    await worker.run()
    print("Worker Started")


if __name__ == "__main__":
    asyncio.run(main(host="127.0.0.1", port=8081, task_queue="my-task-queue", namespace="default"))
