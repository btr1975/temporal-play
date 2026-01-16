"""
activities
"""

import os
import temporalio.workflow
from temporalio.exceptions import ApplicationError
from temporalio import activity
from temporal_play.schemas.schemas import InputData, InputDataNautobotGQLQuery

with temporalio.workflow.unsafe.imports_passed_through():
    from temporal_play.nautobot_gql_client.nautobot_gql_client import NautobotGqlClient
    from temporal_play.hvac_client.hvac_client import HvacClient


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
        obj = NautobotGqlClient(host=secrets["host"], port=8080, token=secrets["token"], ssl_verify=False)
        data = await obj.get_gql_data(query=input_data.query, variables=input_data.variables)

    except Exception as e:
        raise ApplicationError(
            message="",
            non_retryable=False,
        ) from e

    return data


ALL_ACTIVITIES = [
    say_hello_activity,
    get_nautobot_gql_data,
]
