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
class InputDataApprover:
    """Input for an approver"""

    name: str
    approve: bool = False
