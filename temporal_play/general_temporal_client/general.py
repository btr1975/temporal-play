"""
General stuff
"""

import asyncio
from temporalio.client import Client


async def get_workflow_handle(client: Client, workflow_id: str) -> None:
    """Things 2

    :param client: The temporal client object
    :type client: Client
    :param workflow_id: The workflow id
    :type workflow_id: str

    :rtype: None
    :returns: Nothing
    """
    handle = client.get_workflow_handle(workflow_id=workflow_id)

    result = await handle.result()

    describe = await handle.describe()
    history = await handle.fetch_history()

    print(result)
    print(describe)
    print("########################################################################")
    for k in history.to_json_dict().get("events"):
        print(k.keys())
        if k.get("activityTaskScheduledEventAttributes"):
            print(k.get("activityTaskScheduledEventAttributes"))
        if k.get("activityTaskStartedEventAttributes"):
            print(k.get("activityTaskStartedEventAttributes"))


async def get_list_workflows(client: Client) -> None:
    """Things

    :param client: The temporal client object
    :type client: Client

    :rtype: None
    :returns: Nothing
    """
    workflows = client.list_workflows()
    async for item in workflows:
        print(item.id)
        print(item.status.name)
        print(item.workflow_type)
        print(item.task_queue)
        print(item.execution_time)
        print(item.close_time)
        print(item.namespace)


async def main(host: str, port: int) -> None:
    """Main function

    :param host: The temporal host
    :type host: str
    :param port: The temporal port
    :type port: int
    """
    client = await Client.connect(f"{host}:{port}")
    await get_list_workflows(client)
    await get_workflow_handle(client, "run-show-command-workflow-815110bb-11b1-4b3e-9b6a-31f6e1dfb887")


if __name__ == "__main__":
    asyncio.run(main(host="10.0.0.113", port=8081))
