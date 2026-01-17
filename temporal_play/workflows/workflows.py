"""
Workflows
"""

from typing import Sequence
from datetime import timedelta
import logging

from temporalio import workflow
from temporalio.common import RetryPolicy

from temporal_play.schemas.schemas import InputData, InputDataApprover, InputDataNautobotGQLQuery, InputShowCommand

from temporal_play.activities.activities import say_hello_activity, get_nautobot_gql_data, run_show_command_activity


logging.basicConfig(level=logging.INFO)


@workflow.defn(name="say-hello-workflow")
class SayHelloWorkFlow:  # pylint: disable=too-few-public-methods
    """This is a Hello World workflow"""

    @workflow.run
    async def run(self, input_data: InputData) -> str:
        """Method to run the workflow

        :param input_data: Input data
        :type input_data: InputData

        :rtype: str
        :return: Hello World
        """

        return await workflow.execute_activity(
            activity=say_hello_activity,
            arg=input_data,
            schedule_to_close_timeout=timedelta(minutes=10),
        )


@workflow.defn(name="run-nautobot-gql-query-workflow-with-approval")
class RunNautobotGqlQueryWorkflowWithApproval:
    """This is a workflow to get data from Nautobot with an approval signal"""

    def __init__(self) -> None:
        self.approved = None
        self.approver_name = None

    @workflow.run
    async def run(self, input_data: InputDataNautobotGQLQuery) -> dict | str:
        """Method to run the workflow

        :param input_data: Input data
        :type input_data: InputDataNautobotGQLQuery

        :rtype: dict
        :return: Nautobot data
        """

        await workflow.execute_activity(
            activity=say_hello_activity,
            arg=InputData(name="Ben", other="Poo"),
            schedule_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(
                backoff_coefficient=2.0,
                maximum_attempts=5,
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(seconds=2),
            ),
        )

        while True:
            await workflow.wait_condition(lambda: self.approved is not None)

            if self.approved:  # pylint: disable=no-else-break
                break

            else:
                return f"{self.approver_name} put in false"

        return await workflow.execute_activity(
            activity=get_nautobot_gql_data,
            arg=input_data,
            schedule_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(
                backoff_coefficient=2.0,
                maximum_attempts=5,
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(seconds=2),
            ),
        )

    @workflow.signal(name="approval")
    def approval(self, input_data: InputDataApprover) -> None:
        """Approval signal
        A Signal handler mutates the Workflow state but cannot return a value.

        :param input_data: Input data
        :type input_data: InputDataApprover

        :rtype: None
        :returns: Nothing
        """
        self.approved = input_data.approve
        self.approver_name = input_data.name


@workflow.defn(name="run-nautobot-gql-query-workflow")
class RunNautobotGqlQueryWorkflow:  # pylint: disable=too-few-public-methods
    """This is a workflow to get data from Nautobot"""

    @workflow.run
    async def run(self, input_data: InputDataNautobotGQLQuery) -> dict:
        """Method to run the workflow

        :param input_data: Input data
        :type input_data: InputDataNautobotGQLQuery

        :rtype: dict
        :return: Nautobot data
        """

        return await workflow.execute_activity(
            activity=get_nautobot_gql_data,
            arg=input_data,
            schedule_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(
                backoff_coefficient=2.0,
                maximum_attempts=5,
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(seconds=2),
            ),
        )


@workflow.defn(name="run-show-command-workflow")
class RunShowCommandWorkflow:  # pylint: disable=too-few-public-methods
    """This is a workflow to run a show command"""

    @workflow.run
    async def run(self, input_data: InputShowCommand) -> str:
        """Method to run the workflow

        :param input_data: Input data
        :type input_data: InputShowCommand

        :rtype: str
        :return: The show command
        """

        nbot_data = await workflow.execute_activity(
            activity=get_nautobot_gql_data,
            arg=InputDataNautobotGQLQuery(
                query=input_data.nautobot_query.query, variables=input_data.nautobot_query.variables
            ),
            schedule_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(
                backoff_coefficient=2.0,
                maximum_attempts=5,
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(seconds=2),
            ),
        )

        input_data.nbot_query_result = nbot_data

        return await workflow.execute_activity(
            activity=run_show_command_activity,
            arg=input_data,
            schedule_to_close_timeout=timedelta(minutes=10),
            retry_policy=RetryPolicy(
                backoff_coefficient=2.0,
                maximum_attempts=5,
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(seconds=2),
            ),
        )


ALL_WORKFLOWS: Sequence[type] = [
    SayHelloWorkFlow,
    RunNautobotGqlQueryWorkflow,
    RunNautobotGqlQueryWorkflowWithApproval,
    RunShowCommandWorkflow,
]
