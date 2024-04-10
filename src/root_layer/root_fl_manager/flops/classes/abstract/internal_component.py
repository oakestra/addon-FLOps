from api.service_management import append_service_to_flops_project_app, deploy, undeploy
from flops.classes.abstract.oakestratable import FlOpsOakestraBaseClass
from pydantic import Field
from utils.sla.generator import generate_sla


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
        self.service_id = append_service_to_flops_project_app(
            sla=generate_sla(self.sla_components),
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
