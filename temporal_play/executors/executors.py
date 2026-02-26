"""
executors
"""

import asyncio
import uuid

from temporalio.client import Client

from temporal_play.schemas.schemas import (
    InputData,
    InputDataNautobotGQLQuery,
    InputDataApprover,
    InputShowCommand,
    InputRenderConfiguration,
    InputRenderJinja2,
    InputGitRepository,
)


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

QUERY_3 = """
query ($device_name: [String]!) {
  devices(name: $device_name) {
    hostname: name
    primary_ip4 {
			host
    }
    platform {
      network_driver_mappings
    }
  }
}
"""


JINJA_2_TEMPLATE = """
hostname {{ hostname }}
{% for server in config_context.ntp.servers %}
{% if server.preferred is defined and server.preferred %}
  ntp server {{ server.ipv4_host }} preferred
{% else %}
  ntp server {{ server.ipv4_host }}
{% endif %}
{% endfor %}
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


async def run_clone_git_repository_workflow(client: Client, task_queue: str) -> None:
    """Run a workflow run-clone-git-repository-workflow via client.execute_workflow, using that method just
       executes the workflow it does not hand back a handler to deal with signaling and such

    :param client: The temporal client object
    :type client: Client
    :param task_queue: The task queue name
    :type task_queue: str

    :rtype: None
    :returns: Nothing
    """
    result = await client.execute_workflow(
        workflow="run-clone-git-repository-workflow",
        arg=InputGitRepository(repository="https://github.com/btr1975/pyats-genie-command-parse", branch_or_tag=None),
        id=f"run-clone-git-repository-workflow-{uuid.uuid4()}",
        task_queue=task_queue,
    )

    print(f"Workflow Result {result}")


async def run_clone_git_repository_nexus_workflow(client: Client, task_queue: str) -> None:
    """Run a workflow run-clone-git-repository-nexus-workflow via a nexus service, using that method just
       executes the workflow it does not hand back a handler to deal with signaling and such

    :param client: The temporal client object
    :type client: Client
    :param task_queue: The task queue name
    :type task_queue: str

    :rtype: None
    :returns: Nothing
    """
    result = await client.execute_workflow(
        workflow="run-clone-git-repository-nexus-workflow",
        arg=InputGitRepository(repository="https://github.com/btr1975/pyats-genie-command-parse", branch_or_tag=None),
        id=f"run-clone-git-repository-nexus-workflow-{uuid.uuid4()}",
        task_queue=task_queue,
    )

    print(f"Workflow Result {result}")


async def run_show_command_workflow(client: Client, task_queue: str) -> None:
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
        workflow="run-show-command-workflow",
        arg=InputShowCommand(
            command="show interface",
            nautobot_query=InputDataNautobotGQLQuery(query=QUERY_3, variables={"device_name": "3560G_A"}),
        ),
        id=f"run-show-command-workflow-{uuid.uuid4()}",
        task_queue=task_queue,
    )

    print(f"Workflow Result {result}")


async def run_render_configuration_workflow(client: Client, task_queue: str) -> None:
    """Run a workflow run-render-configuration-workflow via client.execute_workflow, using that method just
       executes the workflow it does not hand back a handler to deal with signaling and such

    :param client: The temporal client object
    :type client: Client
    :param task_queue: The task queue name
    :type task_queue: str

    :rtype: None
    :returns: Nothing
    """
    result = await client.execute_workflow(
        workflow="run-render-configuration-workflow",
        arg=InputRenderConfiguration(
            jinja_2=InputRenderJinja2(template=JINJA_2_TEMPLATE, variable_data={}),
            nautobot_query=InputDataNautobotGQLQuery(
                query=QUERY, variables={"device_name": ["3560G_A", "3560G_B", "3560G_C", "3560G_D"]}
            ),
        ),
        id=f"run-render-configuration-workflow-{uuid.uuid4()}",
        task_queue=task_queue,
    )

    print(f"Workflow Result {result}")


async def run_render_configuration_nexus_workflow(client: Client, task_queue: str) -> None:
    """Run a workflow run-render-configuration-nexus-workflow via a nexus client, using that method just
       executes the workflow it does not hand back a handler to deal with signaling and such

    :param client: The temporal client object
    :type client: Client
    :param task_queue: The task queue name
    :type task_queue: str

    :rtype: None
    :returns: Nothing
    """
    result = await client.execute_workflow(
        workflow="run-render-configuration-nexus-workflow",
        arg=InputRenderConfiguration(
            jinja_2=InputRenderJinja2(template=JINJA_2_TEMPLATE, variable_data={}),
            nautobot_query=InputDataNautobotGQLQuery(
                query=QUERY, variables={"device_name": ["3560G_A", "3560G_B", "3560G_C", "3560G_D"]}
            ),
        ),
        id=f"run-render-configuration-nexus-workflow-{uuid.uuid4()}",
        task_queue=task_queue,
    )

    print(f"Workflow Result {result}")


async def run_nautobot_gql_query_workflow_with_approval(client: Client, task_queue: str) -> None:
    """Run a run-nautobot-gql-query-workflow-with-approval via client.start_workflow, using that method
       gives back a handler to deal with signaling and such, also this is how you start a workflow without
       waiting fo it complete

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


async def main(host: str, port: int, task_queue: str, namespace: str) -> None:
    """Main function

    :param host: The temporal host
    :type host: str
    :param port: The temporal port
    :type port: int
    :param task_queue: The name of the task queue
    :type task_queue: str
    :param namespace: The namespace
    :type namespace: str

    :rtype: None
    :returns: Nothing
    """
    client = await Client.connect(f"{host}:{port}", namespace=namespace)
    await run_render_configuration_nexus_workflow(client=client, task_queue=task_queue)


async def main_run_multiple(host: str, port: int, task_queue: str, namespace: str) -> None:
    """Main function

    :param host: The temporal host
    :type host: str
    :param port: The temporal port
    :type port: int
    :param task_queue: The name of the task queue
    :type task_queue: str
    :param namespace: The namespace
    :type namespace: str

    :rtype: None
    :returns: Nothing
    """
    client = await Client.connect(f"{host}:{port}", namespace=namespace)

    tasks = []
    for _ in range(10):
        tasks.append(run_render_configuration_workflow(client=client, task_queue=task_queue))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main(host="10.0.0.113", port=8081, task_queue="my-task-queue", namespace="namespace-2"))
