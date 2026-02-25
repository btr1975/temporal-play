"""
Nexus workers
"""

import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from temporal_play.nexus.handlers.handlers import MyNexusServicesHandler
from temporal_play.workflows.workflows import RunCloneGitRepositoryWorkflow


def get_nexus_worker(client: Client, task_queue: str) -> Worker:
    """Get a Nexus worker

    :param client: Nexus client
    :param task_queue: Nexus task queue

    :return: Nexus worker
    """
    print("Starting Nexus Worker")
    worker = Worker(
        client=client,
        task_queue=task_queue,
        workflows=[RunCloneGitRepositoryWorkflow],
        nexus_service_handlers=[MyNexusServicesHandler()],
    )

    return worker


async def main(host: str, port: int | str, task_queue: str, namespace: str) -> None:
    """Main function

    :param host: Nexus server address
    :param port: Nexus server port
    :param task_queue: Nexus task queue
    :param namespace: Nexus namespace

    :returns: Nothing
    """
    client = await Client.connect(target_host=f"{host}:{port}", namespace=namespace)
    worker = get_nexus_worker(client=client, task_queue=task_queue)
    await worker.run()
    print("Nexus Worker Started")


if __name__ == "__main__":
    asyncio.run(main(host="localhost", port=8081, task_queue="my-task-queue", namespace="default"))
