"""
Workflows
"""

from typing import Sequence
from datetime import timedelta
from dataclasses import dataclass

from temporalio import workflow

from temporal_play.activities.activities import say_hello_activity, get_nautobot_gql_data


@dataclass
class InputData:
    name: str
    other: str


@dataclass
class NautobotGQLQueryInput:
    query: str
    variables: dict | None


@workflow.defn(name="say-hello-workflow")
class SayHelloWorkFlow:

    @workflow.run
    async def run(self, input_data: InputData) -> str:

        return await workflow.execute_activity(
            activity=say_hello_activity,
            arg=input_data.name,
            schedule_to_close_timeout=timedelta(minutes=10),
        )


@workflow.defn(name="run-nautobot-gql-query-workflow")
class RunNautobotGqlQueryWorkflow:

    @workflow.run
    async def run(self, input_data: NautobotGQLQueryInput) -> str:

        return await workflow.execute_activity(
            activity=get_nautobot_gql_data,
            arg={"query": input_data.query, "variables": input_data.variables},
            schedule_to_close_timeout=timedelta(minutes=10),
        )


ALL_WORKFLOWS: Sequence[type] = [SayHelloWorkFlow, RunNautobotGqlQueryWorkflow]
