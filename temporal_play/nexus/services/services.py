"""
Nexus services
"""

import nexusrpc

from temporal_play.schemas.schemas import InputGitRepository, InputRenderConfiguration


@nexusrpc.service(name="nexus-my-nexus-services")
class MyNexusServices:
    """Temporal Nexus Services
    This defines operations available to the handler

    :cvar clone: nexusrpc.Operation[InputGitRepository, str]
    :cvar render_config: nexusrpc.Operation[InputRenderConfiguration, tuple[str]]
    """

    clone: nexusrpc.Operation[InputGitRepository, str]
    render_config: nexusrpc.Operation[InputRenderConfiguration, tuple[str]]
