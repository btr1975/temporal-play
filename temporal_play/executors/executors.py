"""
executors
"""

import asyncio
import uuid

from temporalio.client import Client

from temporal_play.schemas.schemas import InputData, InputDataNautobotGQLQuery, InputDataApprover


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

QUERY_2 = """
query {
  devices {
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


async def run_say_hello_workflow(client: Client, task_queue: str) -> None:
    """Run a say-hello-workflow via client.execute_workflow, using that method just executes the workflow
       it does not hand back a handler to deal with signaling and such

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


async def run_nautobot_gql_query_workflow(client: Client, task_queue: str) -> None:
    """Run a workflow run-nautobot-gql-query-workflow via client.execute_workflow, using that method just
       executes the workflow it does not hand back a handler to deal with signaling and such

    :param client: The temporal client object
    :type client: Client
    :param task_queue: The task queue name
    :type task_queue: str

    :rtype: None
    :returns: Nothing
    """
    result = await client.execute_workflow(
        workflow="run-nautobot-gql-query-workflow",
        arg=InputDataNautobotGQLQuery(query=QUERY_2, variables=None),
        id=f"run-nautobot-gql-query-workflow-{uuid.uuid4()}",
        task_queue=task_queue,
    )

    print(f"Workflow Result {result}")


async def run_nautobot_gql_query_workflow_with_approval(client: Client, task_queue: str) -> None:
    """Run a run-nautobot-gql-query-workflow-with-approval via client.start_workflow, using that method
       gives back a handler to deal with signaling and such

    :param client: The temporal client object
    :type client: Client
    :param task_queue: The task queue name
    :type task_queue: str

    :rtype: None
    :returns: Nothing
    """
    handler = await client.start_workflow(
        workflow="run-nautobot-gql-query-workflow-with-approval",
        arg=InputDataNautobotGQLQuery(query=QUERY_2, variables=None),
        id=f"run-nautobot-gql-query-workflow-with-approval-{uuid.uuid4()}",
        task_queue=task_queue,
    )

    await handler.signal(signal="approval", arg=InputDataApprover(name="Ben", approve=True))

    result = await handler.result()

    print(f"Workflow Result {result}")


async def main(host: str, port: int, task_queue: str) -> None:
    """Main function

    :param host: The temporal host
    :type host: str
    :param port: The temporal port
    :type port: int
    :param task_queue: The name of the task queue
    :type task_queue: str
    """
    client = await Client.connect(f"{host}:{port}")
    await run_say_hello_workflow(client=client, task_queue=task_queue)


if __name__ == "__main__":
    asyncio.run(main(host="10.0.0.113", port=8081, task_queue="my-task-queue"))
