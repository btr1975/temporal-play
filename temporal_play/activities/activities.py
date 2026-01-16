"""
activities
"""

import temporalio.workflow
from temporalio.exceptions import ApplicationError
from temporalio import activity
from temporal_play.schemas.schemas import InputData, InputDataNautobotGQLQuery

with temporalio.workflow.unsafe.imports_passed_through():
    from temporal_play.nautobot_gql_client.nautobot_gql_client import NautobotGqlClient


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
        obj = NautobotGqlClient(
            host="http://10.0.0.113", port=8080, token="0123456789abcdef0123456789abcdef01234567", ssl_verify=False
        )
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
