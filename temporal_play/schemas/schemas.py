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
    host: str | None = None
    device_type: str | None = None
    nbot_query_result: dict | None = None


@dataclass
class InputDataApprover:
    """Input for an approver"""

    name: str
    approve: bool = False
