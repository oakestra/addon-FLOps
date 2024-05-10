from flops_manager.classes.apps.observatory import FLOpsObservatory
from flops_manager.classes.services.service_base import FLOpsService
from flops_manager.mlflow.storages.backend_stores import get_user_backend_store_uri
from flops_manager.utils.common import generate_ip, get_shortened_unique_id
from flops_manager.utils.sla.components import (
    SlaComponentsWrapper,
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
)
from pydantic import AliasChoices, Field

TRACKING_SERVER_PORT = 7027


class TrackingServer(FLOpsService):
    namespace = "tracking"

    parent_app: FLOpsObservatory = Field(None, exclude=True, repr=False)
    customer_id: str = Field(alias=AliasChoices("customer_id", "customerID"))

    ip: str = Field("", init=False)

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        self.ip = generate_ip(self.parent_app.app_id, self)
        super().model_post_init(_)

    def get_url(self) -> str:
        return f"http://{self.ip}:{TRACKING_SERVER_PORT}"

    def _configure_sla_components(self) -> None:
        service_name = f"tracking{get_shortened_unique_id(self.parent_app.customer_id)}"
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=self.parent_app.customer_id,
                app_id=self.parent_app.app_id,
                names=SlaNames(
                    app_name=self.parent_app.app_name,
                    app_namespace=self.parent_app.namespace,
                    service_name=service_name,
                    service_namespace=self.namespace,
                ),
                compute=SlaCompute(
                    code="ghcr.io/malyuk-a/tracking-server:latest",
                    cmd=" ".join(
                        (
                            "mlflow",
                            "server",
                            "--backend-store-uri",
                            get_user_backend_store_uri(self.parent_app.customer_id),
                            "--host",
                            "0.0.0.0",
                            "--port",
                            str(TRACKING_SERVER_PORT),
                            "--serve-artifacts",
                            "--artifacts-destination",
                            "ftp://flops:flops@192.168.178.44/flops_artifacts",
                        )
                    ),
                ),
            ),
            details=SlaDetails(
                rr_ip=self.ip,
                resources=SlaResources(memory=200, vcpus=1, storage=0),
                port=str(TRACKING_SERVER_PORT),
            ),
        )
