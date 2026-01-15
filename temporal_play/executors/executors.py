"""
executors
"""

import asyncio
import uuid

from temporalio.client import Client

from temporal_play.workflows.workflows import InputData


async def run_workflow(client: Client) -> None:
    """Run a workflow

    :param client: The temporal client object
    :type client: Client

    :rtype: None
    :returns: Nothing
    """
    result = await client.execute_workflow(
        workflow="say-hello-workflow",
        arg=InputData(name="Mooo", other="Moo Other"),
        id=f"say-hello-workflow-{uuid.uuid4()}",
        task_queue="my-task-queue",
    )
    print(f"Workflow Result {result}")


async def main():
    client = await Client.connect("localhost:8081")
    await run_workflow(client)


if __name__ == "__main__":
    asyncio.run(main())
