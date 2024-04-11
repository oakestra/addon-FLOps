import flops_manager.api.service_management as service_management
from flops_manager.flops.classes.abstract.oakestratable import FlOpsOakestraBaseClass
from pydantic import Field


class DeployableClass(FlOpsOakestraBaseClass):
    """Adds functionality of services like (Un)Deployment."""

    service_id: str = Field("", init=False)

    def model_post_init(self, _) -> None:
        if self.gets_loaded_from_db:
            return

        super().model_post_init(_)
        self.deploy()

    def deploy(self) -> None:
        service_management.deploy(service_id=self.service_id, matching_caller_object=self)

    def undeploy(self) -> None:
        service_management.undeploy(
            application_id=self.app_id,
            flops_project_id=self.flops_project_id,
            matching_caller_object=self,
        )
