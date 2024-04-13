from abc import ABC

from flops_manager.api.service_management import deploy, undeploy
from flops_manager.classes.oakestratables.base import FlOpsOakestraBaseClass
from pydantic import Field


class DeployableClass(FlOpsOakestraBaseClass, ABC):
    """Adds functionality of services like (Un)Deployment."""

    service_id: str = Field("", init=False)

    bearer_token: str = Field("", exclude=True, repr=False)

    def model_post_init(self, _) -> None:
        if self.gets_loaded_from_db:
            return

        super().model_post_init(_)
        self.deploy()

    def deploy(self) -> None:
        deploy(service_id=self.service_id, matching_caller_object=self)

    def undeploy(self) -> None:
        undeploy(
            application_id=self.app_id,
            matching_caller_object=self,
        )
