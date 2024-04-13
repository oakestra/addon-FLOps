from flops_manager.classes.oakestratables.deployables.base import DeployableClass
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


class FLOpsImageRegistry(DeployableClass):
    """'Singleton' of a docker registry container that will be shared by every FLOps project."""

    ip: str = Field("", init=False)

    namespace = "flopsir"

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        # self.ip = generate_ip(self.flops_project_id, self)
        self.ip = "10.30.27.27"
        super().model_post_init(_)

    def _configure_sla_components(self) -> None:
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(
                    app_name=self.namespace,
                    app_namespace=self.namespace,
                    service_name=self.namespace,
                    service_namespace=self.namespace,
                ),
                compute=SlaCompute(
                    code="ghcr.io/malyuk-a/flops-image-registry:latest",
                    cmd=FLOPS_SERVICE_CMD_PREFIX,
                ),
            ),
            details=SlaDetails(
                rr_ip=self.ip,
                resources=SlaResources(memory=200, vcpus=1, storage=1000),
            ),
        )
