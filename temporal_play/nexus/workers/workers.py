"""
Nexus workers
"""

import asyncio


from temporalio.client import Client


from temporal_play.nexus.workers.nexus_worker_creator import get_nexus_worker
from temporal_play.nexus.handlers.handlers import MyNexusServicesHandler
from temporal_play.workflows.workflows import ALL_WORKFLOWS_FOR_NEXUS_WORKERS


async def main(host: str, port: int | str, task_queue: str, namespace: str) -> None:
    """Main function

    :param host: Nexus server address
    :param port: Nexus server port
    :param task_queue: Nexus task queue
    :param namespace: Nexus namespace

    :returns: Nothing
    """
    client = await Client.connect(target_host=f"{host}:{port}", namespace=namespace)
    worker = get_nexus_worker(
        client=client,
        task_queue=task_queue,
        workflows=ALL_WORKFLOWS_FOR_NEXUS_WORKERS,
        nexus_service_handlers=[MyNexusServicesHandler()],
    )
    await worker.run()
    print("Nexus Worker Started")


if __name__ == "__main__":
    asyncio.run(main(host="localhost", port=8081, task_queue="my-task-queue", namespace="default"))
