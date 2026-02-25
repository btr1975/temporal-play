"""
Nexus services
"""

import nexusrpc

from temporal_play.schemas.schemas import InputGitRepository


@nexusrpc.service(name="nexus-my-nexus-services")
class MyNexusServices:
    """Temporal Nexus Services
    This defines operations available to the handler

    :cvar clone: nexusrpc.Operation[InputGitRepository, str]
    """

    clone: nexusrpc.Operation[InputGitRepository, str]
