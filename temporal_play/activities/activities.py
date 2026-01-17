"""
activities
"""

import os
import temporalio.workflow
from temporalio.exceptions import ApplicationError
from temporalio import activity
from temporal_play.schemas.schemas import InputData, InputDataNautobotGQLQuery, InputShowCommand

with temporalio.workflow.unsafe.imports_passed_through():
    from temporal_play.nautobot_gql_client.nautobot_gql_client import NautobotGqlClient
    from temporal_play.hvac_client.hvac_client import HvacClient
    from temporal_play.netmiko_client.netmiko_client import NetmikoClient


@activity.defn(name="say-hello-activity")
async def say_hello_activity(input_data: InputData) -> str:
    """A Hello World activity

    :param input_data: input data
    :type input_data: InputData

    :rtype: str
    :return: Hello
    """
    try:
        activity.logger.info(f"Hello {input_data.name}")

    except Exception as e:
        raise ApplicationError(
            message=f"Hello {input_data.name}",
            non_retryable=False,
        ) from e

    return f"Hello {input_data.other}"


@activity.defn(name="get-nautobot-gql-data")
async def get_nautobot_gql_data(input_data: InputDataNautobotGQLQuery) -> dict:
    """This activity gets nautobot data using a GraphQL query

    :param input_data: input data
    :type input_data: InputDataNautobotGQLQuery

    :rtype: dict
    :return: nautobot gql data
    """
    try:
        secrets_client = HvacClient(
            host=os.getenv("HVAC_HOST"), port=os.getenv("HVAC_PORT"), token=os.getenv("HVAC_TOKEN")
        )
        secrets = await secrets_client.get_secret("/nautobot")
        obj = NautobotGqlClient(host=secrets["host"], port=secrets["port"], token=secrets["token"], ssl_verify=False)
        data = await obj.get_gql_data(query=input_data.query, variables=input_data.variables)

    except Exception as e:
        raise ApplicationError(
            message="",
            non_retryable=False,
        ) from e

    return data


@activity.defn(name="run-show-command-activity")
async def run_show_command_activity(input_data: InputShowCommand) -> str:
    """This activity runs a show command using Netmiko

    :param input_data: input data
    :type input_data: InputShowCommand

    :rtype: str
    :return: The result of show command
    """
    try:
        secrets_client = HvacClient(
            host=os.getenv("HVAC_HOST"), port=os.getenv("HVAC_PORT"), token=os.getenv("HVAC_TOKEN")
        )
        device_secrets = await secrets_client.get_secret("/devices")
        device_type = input_data.nbot_query_result["data"]["devices"][0]["platform"]["network_driver_mappings"][
            "netmiko"
        ]
        host = input_data.nbot_query_result["data"]["devices"][0]["primary_ip4"]["address"].split("/")[0]
        device = NetmikoClient(
            host=host, username=device_secrets["username"], password=device_secrets["password"], device_type=device_type
        )
        data = await device.send_command(input_data.command)

    except Exception as e:
        raise ApplicationError(
            message="",
            non_retryable=False,
        ) from e

    return data


ALL_ACTIVITIES = [
    say_hello_activity,
    get_nautobot_gql_data,
    run_show_command_activity,
]
