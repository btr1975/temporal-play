"""
Nexus handlers
"""

import uuid
import nexusrpc.handler
from temporalio import nexus

from temporal_play.nexus.services.services import MyNexusServices
from temporal_play.schemas.schemas import InputGitRepository


@nexusrpc.handler.service_handler(service=MyNexusServices)
class MyNexusServicesHandler:
    """Nexus services handler"""

    @nexus.workflow_run_operation
    async def clone(
        self, ctx: nexus.WorkflowRunOperationContext, input_data: InputGitRepository
    ) -> nexus.WorkflowHandle[str]:
        """Implementation of the clone operation

        :param ctx: Nexus workflow run context
        :param input_data: Nexus workflow run input data
        """

        return await ctx.start_workflow(
            workflow="run-clone-git-repository-workflow",
            arg=input_data,
            id=f"nexus-run-clone-git-repository-workflow-{str(uuid.uuid4())}",
        )
