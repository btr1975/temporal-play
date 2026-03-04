"""
activities
"""

import os
import tempfile
from pathlib import Path
import temporalio.workflow
from temporalio.exceptions import ApplicationError
from temporalio import activity
from temporal_play.schemas.schemas import (
    InputData,
    InputDataNautobotGQLQuery,
    InputNetmikoCommand,
    InputRenderJinja2,
    InputGitRepository,
)

with temporalio.workflow.unsafe.imports_passed_through():
    from temporal_play.nautobot_gql_client.nautobot_gql_client import NautobotGqlClient
    from temporal_play.hvac_client.hvac_client import HvacClient
    from temporal_play.netmiko_client.netmiko_client import NetmikoClient
    from temporal_play.rendering.rendering import render_jinja2_template
    from temporal_play.git_client.git_client import GitClient


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
async def run_show_command_activity(input_data: InputNetmikoCommand) -> str:
    """This activity runs a show command using Netmiko

    :param input_data: input data
    :type input_data: InputNetmikoCommand

    :rtype: str
    :return: The result of show command
    """
    try:
        secrets_client = HvacClient(
            host=os.getenv("HVAC_HOST"), port=os.getenv("HVAC_PORT"), token=os.getenv("HVAC_TOKEN")
        )
        device_secrets = await secrets_client.get_secret("/devices")

        device = NetmikoClient(
            host=input_data.host,
            username=device_secrets["username"],
            password=device_secrets["password"],
            device_type=input_data.device_type,
        )

        data = await device.send_command(input_data.command)

    except Exception as e:
        raise ApplicationError(
            message="",
            non_retryable=False,
        ) from e

    return data


@activity.defn(name="run-show-command-parse-with-ntc-template-activity")
async def run_show_command_parse_with_ntc_templates_activity(input_data: InputNetmikoCommand) -> list[dict]:
    """This activity runs a show command using Netmiko and parses with ntc-templates

    :param input_data: input data
    :type input_data: InputNetmikoCommand

    :rtype: list[dict]
    :return: The result of show command
    """
    try:
        secrets_client = HvacClient(
            host=os.getenv("HVAC_HOST"), port=os.getenv("HVAC_PORT"), token=os.getenv("HVAC_TOKEN")
        )
        device_secrets = await secrets_client.get_secret("/devices")

        device = NetmikoClient(
            host=input_data.host,
            username=device_secrets["username"],
            password=device_secrets["password"],
            device_type=input_data.device_type,
        )

        data = await device.send_command_parse_ntc_templates(input_data.command)

    except Exception as e:
        raise ApplicationError(
            message="",
            non_retryable=False,
        ) from e

    return data


@activity.defn(name="run-render-jinja2-activity")
async def run_render_jinja2_activity(input_data: InputRenderJinja2) -> str:
    """This activity renders from Jinja2

    :param input_data: input data
    :type input_data: InputRenderJinja2

    :rtype: str
    :return: The rendered template
    """
    try:
        data = await render_jinja2_template(template=input_data.template, variable_data=input_data.variable_data)

    except Exception as e:
        raise ApplicationError(
            message="",
            non_retryable=False,
        ) from e

    return data


@activity.defn(name="run-clone-git-repository-activity")
async def run_clone_git_repository_activity(input_data: InputGitRepository) -> str:
    """This activity clones a git repository

    :param input_data: input data
    :type input_data: InputGitRepository

    :rtype: str
    :return: The cloned path
    """
    try:
        activity_id = activity.info().activity_id
        workflow_run_id = activity.info().workflow_run_id
        secrets_client = HvacClient(
            host=os.getenv("HVAC_HOST"), port=os.getenv("HVAC_PORT"), token=os.getenv("HVAC_TOKEN")
        )
        github_secrets = await secrets_client.get_secret("/github")

        clone_path = Path(tempfile.gettempdir()) / f"{workflow_run_id}-{activity_id}"

        git_client = GitClient(
            username="__token__",
            password=github_secrets["token"],
            repository=input_data.repository,
            clone_path=clone_path.as_posix(),
        )

        await git_client.clone(branch_or_tag=input_data.branch_or_tag)

    except Exception as e:
        raise ApplicationError(
            message="",
            non_retryable=False,
        ) from e

    return clone_path.as_posix()


ALL_ACTIVITIES = [
    say_hello_activity,
    get_nautobot_gql_data,
    run_show_command_activity,
    run_show_command_parse_with_ntc_templates_activity,
    run_render_jinja2_activity,
    run_clone_git_repository_activity,
]
