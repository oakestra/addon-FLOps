from abc import ABC

from flops_manager.api.service_management import append_service_to_app, deploy, undeploy
from flops_manager.classes.apps.app_base import FLOpsApp
from flops_manager.classes.base import FlOpsOakestraBaseClass
from flops_manager.database.common import remove_from_db_by_project_id
from flops_manager.utils.sla.generator import generate_sla
from pydantic import AliasChoices, Field


class FLOpsService(FlOpsOakestraBaseClass, ABC):
    """Represents a service in the orchestrator which will be added to a FLOpsApp."""

    parent_app: FLOpsApp = Field(None, exclude=True, repr=False)

    service_id: str = Field("", init=False, alias=AliasChoices("service_id", "microserviceID"))
    bearer_token: str = Field("", exclude=True, repr=False)

    def model_post_init(self, _) -> None:
        if self.gets_loaded_from_db:
            return

        super().model_post_init(_)
        self.deploy()

    def _create_in_orchestrator(self) -> None:
        self.service_id = append_service_to_app(
            sla=generate_sla(self.sla_components),
            bearer_token=getattr(self, "bearer_token", None),
            app_id=self.parent_app.app_id,
            matching_caller_object=self,
        )

    def deploy(self) -> None:
        deploy(service_id=self.service_id, matching_caller_object=self)

    def undeploy(self) -> None:
        undeploy(service_id=self.service_id, matching_caller_object=self)
        remove_from_db_by_project_id(FLOpsService, self.flops_project_id)
