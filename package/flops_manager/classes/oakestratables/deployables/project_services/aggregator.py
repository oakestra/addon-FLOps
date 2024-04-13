from flops_manager.classes.oakestratables.deployables.project_services.base import (
    FLOpsProjectService,
)
from flops_manager.classes.oakestratables.project import FlOpsProject
from flops_manager.mqtt.sender import notify_ui
from flops_manager.utils.common import generate_ip
from flops_manager.utils.constants import FLOPS_SERVICE_CMD_PREFIX, FLOPS_USER_ACCOUNT
from flops_manager.utils.sla.components import (
    SlaComponentsWrapper,
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
)
from pydantic import Field


class FLAggregator(FLOpsProjectService):
    flops_project: FlOpsProject = Field(None, exclude=True, repr=False)

    flops_project_id: str = Field("", init=False)

    ip: str = Field("", init=False)

    namespace = "flaggreg"

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        if self.flops_project.verbose:
            notify_ui(
                flops_project_id=self.flops_project_id,
                msg="Preparing new FL Aggregator.",
            )

        self.flops_project_id = self.flops_project.flops_project_id
        self.ip = generate_ip(self.flops_project_id, self)
        super().model_post_init(_)

        if self.flops_project.verbose:
            notify_ui(
                flops_project_id=self.flops_project_id,
                msg="New Aggregator service created & deployed",
            )

    def _configure_sla_components(self) -> None:
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                app_id=self.flops_project_id,
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(
                    app_name=self.flops_project.project_app_name,
                    app_namespace=self.flops_project.namespace,
                    service_name=f"ag{self.flops_project.get_shortened_id()}",
                    service_namespace=self.namespace,
                ),
                compute=SlaCompute(
                    code="ghcr.io/malyuk-a/fl-aggregator:latest",
                    one_shot_service=True,
                    cmd=FLOPS_SERVICE_CMD_PREFIX,
                ),
            ),
            details=SlaDetails(
                rr_ip=self.ip,
                resources=SlaResources(
                    memory=100,
                    vcpus=1,
                    storage=0,
                ),
            ),
        )
