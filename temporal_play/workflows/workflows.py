"""
Workflows
"""

from typing import Sequence
from datetime import timedelta
from dataclasses import dataclass

from temporalio import workflow

from temporal_play.activities.activities import say_hello_activity


@dataclass
class InputData:
    name: str
    other: str


@workflow.defn(name="say-hello-workflow")
class SayHelloWorkFlow:

    @workflow.run
    async def run(self, input_data: InputData) -> str:

        return await workflow.execute_activity(
            activity=say_hello_activity,
            arg=input_data.name,
            schedule_to_close_timeout=timedelta(minutes=10),
        )


ALL_WORKFLOWS: Sequence[type] = [SayHelloWorkFlow]
