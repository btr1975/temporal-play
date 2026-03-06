"""
Worker that consumes ONLY nexus workflows
"""

import asyncio

from temporal_play.client_factory import BasicClientFactory
from temporal_play.activities.activities import ALL_ACTIVITIES
from temporal_play.workflows.workflows import ALL_NEXUS_WORKFLOWS


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
    worker = await BasicClientFactory.create(host=host, port=port, namespace=namespace).get_worker(
        task_queue=task_queue, workflows=ALL_NEXUS_WORKFLOWS, activities=ALL_ACTIVITIES
    )

    await worker.run()
    print("Worker Started")


if __name__ == "__main__":
    asyncio.run(main(host="127.0.0.1", port=8081, task_queue="my-task-queue", namespace="default"))
