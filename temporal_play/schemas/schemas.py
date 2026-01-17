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
class InputDataApprover:
    """Input for an approver"""

    name: str
    approve: bool = False
