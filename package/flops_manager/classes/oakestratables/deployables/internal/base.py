from flops_manager.api.service_management import (
    append_service_to_flops_project_app,
    deploy,
    undeploy,
)
from flops_manager.classes.oakestratables.base import FlOpsOakestraBaseClass
from flops_manager.utils.sla.generator import generate_sla
from pydantic import Field


class InternalProjectComponent(FlOpsOakestraBaseClass):
    """A class for internal FLOps components.
    Such a component can be created & deployed only as a service.
    This service will be appended to an already existing FLOps project application.
    """

    service_id: str = Field("", init=False)

    def model_post_init(self, _) -> None:
        if self.gets_loaded_from_db:
            return

        super().model_post_init(_)
        self.deploy()

    def create(self) -> None:
        from icecream import ic

        sla = generate_sla(self.sla_components)
        ic("Reeeeeee", sla)

        self.service_id = append_service_to_flops_project_app(
            sla=sla,
            bearer_token=getattr(self, "bearer_token", None),
            flops_project_id=self.flops_project_id,
            matching_caller_object=self,
        )

    def deploy(self) -> None:
        deploy(service_id=self.service_id, matching_caller_object=self)

    def undeploy(self) -> None:
        undeploy(
            service_id=self.service_id,
            flops_project_id=self.flops_project_id,
            matching_caller_object=self,
        )
