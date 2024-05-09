from abc import ABC

from flops_manager.api.service_management import deploy, undeploy
from flops_manager.classes.project_based import FlOpsOakestraProjectBasedClass
from flops_manager.database.common import remove_from_db_by_project_id
from pydantic import AliasChoices, Field


class DeployableClass(FlOpsOakestraProjectBasedClass, ABC):
    """Adds functionality of services like (Un)Deployment."""

    service_id: str = Field("", init=False, alias=AliasChoices("service_id", "microserviceID"))

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
            service_id=self.service_id,
            matching_caller_object=self,
            flops_project_id=self.flops_project_id,
        )
        remove_from_db_by_project_id(DeployableClass, self.flops_project_id)
