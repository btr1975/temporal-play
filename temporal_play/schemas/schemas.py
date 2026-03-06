"""
schemas
"""

from dataclasses import dataclass


@dataclass
class InputData:
    """A data set"""

    name: str
    other: str


@dataclass
class InputDataNautobotGQLQuery:
    """Input to run a Nautobot GQL query"""

    query: str
    variables: dict | None


@dataclass
class InputShowCommand:
    """Input to run a show command"""

    command: str
    nautobot_query: InputDataNautobotGQLQuery


@dataclass
class InputNetmikoCommand:
    """Input to run a Netmiko command"""

    command: str
    host: str
    device_type: str


@dataclass
class InputRenderJinja2:
    """Input to render a Jinja2 template"""

    template: str
    variable_data: dict


@dataclass
class InputRenderConfiguration:
    """Input to render a configuration file"""

    jinja_2: InputRenderJinja2
    nautobot_query: InputDataNautobotGQLQuery


@dataclass
class InputDataApprover:
    """Input for an approver"""

    name: str
    approve: bool


@dataclass
class InputGitRepository:
    """Input for a git repository"""

    repository: str
    branch_or_tag: str | None = None
