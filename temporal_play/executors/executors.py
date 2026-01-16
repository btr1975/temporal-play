"""
executors
"""

import asyncio
import uuid

from temporalio.client import Client

from temporal_play.workflows.workflows import InputData, NautobotGQLQueryInput


QUERY = """
query ($device_name: [String]!) {
  devices(name: $device_name) {
    hostname: name
    config_context
    interfaces {
      name
      untagged_vlan {
        id
        vid
        name
      }
      tagged_vlans {
        id
        vid
        name
      }
    }
  }
}
"""


async def run_workflow(client: Client, task_queue: str) -> None:
    """Run a workflow

    :param client: The temporal client object
    :type client: Client
    :param task_queue: The task queue name
    :type task_queue: str

    :rtype: None
    :returns: Nothing
    """
    result = await client.execute_workflow(
        workflow="say-hello-workflow",
        arg=InputData(name="Mooo", other="Moo Other"),
        id=f"say-hello-workflow-{uuid.uuid4()}",
        task_queue=task_queue,
    )
    print(f"Workflow Result {result}")


async def run_workflow_2(client: Client, task_queue: str) -> None:
    """Run a workflow

    :param client: The temporal client object
    :type client: Client
    :param task_queue: The task queue name
    :type task_queue: str

    :rtype: None
    :returns: Nothing
    """
    result = await client.execute_workflow(
        workflow="run-nautobot-gql-query-workflow",
        arg=NautobotGQLQueryInput(query=QUERY, variables={"device_name": "3560G_A"}),
        id=f"run-nautobot-gql-query-workflow-{uuid.uuid4()}",
        task_queue=task_queue,
    )
    print(f"Workflow Result {result}")

async def main(host: str, port: int, task_queue: str):
    client = await Client.connect(f"{host}:{port}")
    await run_workflow_2(client=client, task_queue=task_queue)


if __name__ == "__main__":
    asyncio.run(main(host="10.0.0.113", port=8081, task_queue="my-task-queue"))
