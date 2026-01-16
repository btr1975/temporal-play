"""
activities
"""
import temporalio.workflow
from temporalio import activity

with temporalio.workflow.unsafe.imports_passed_through():
    from temporal_play.nautobot_gql_client.nautobot_gql_client import NautobotGqlClient


@activity.defn(name="say-hello-activity")
async def say_hello_activity(name: str) -> str:
    activity.logger.info("Hello {}".format(name))
    return f"Hello {name}"


@activity.defn(name="get-nautobot-gql-data")
async def get_nautobot_gql_data(query: str, variables: dict = None) -> dict:
    obj = NautobotGqlClient(
        host="http://10.0.0.113", port=8080, token="0123456789abcdef0123456789abcdef01234567", ssl_verify=False
    )
    data = await obj.get_gql_data(query=query, variables=variables)

    return data


ALL_ACTIVITIES = [
    say_hello_activity,
    get_nautobot_gql_data,
]
