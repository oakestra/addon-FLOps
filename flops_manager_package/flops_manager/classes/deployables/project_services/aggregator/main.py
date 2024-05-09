from flops_manager.classes.deployables.project_services.base import FLOpsProjectService
from flops_manager.image_management import FLOpsImageTypes, get_flops_image_name
from flops_manager.mlflow.tracking_server import get_mlflow_tracking_server_url
from flops_manager.mqtt.constants import FLOPS_MQTT_BROKER_IP
from flops_manager.mqtt.sender import notify_ui
from flops_manager.utils.common import generate_ip, get_shortened_id
from flops_manager.utils.constants import FLOPS_USER_ACCOUNT
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
    flops_ui_ip: str = Field("", exclude=True, repr=False)

    ip: str = Field("", init=False)

    fl_aggregator_image: str = Field("", init=False)

    namespace = "aggr"

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        self.flops_project_id = self.flops_project.flops_project_id
        if self.flops_project.verbose:
            notify_ui(
                flops_project_id=self.flops_project_id,
                msg="Preparing new FL Aggregator.",
            )
        self.ip = generate_ip(self.flops_project_id, self)
        self.fl_aggregator_image = get_flops_image_name(
            ml_repo_info=self.flops_project.ml_repo_info,
            flops_image_type=FLOpsImageTypes.AGGREGATOR,
        )

        super().model_post_init(_)
        if self.flops_project.verbose:
            notify_ui(
                flops_project_id=self.flops_project_id,
                msg="New Aggregator service created & deployed",
            )

    def configure_sla_components(self) -> None:
        training_conf = self.flops_project.training_configuration
        cmd = " ".join(
            (
                "python",
                "main.py",
                self.flops_project_id,
                FLOPS_MQTT_BROKER_IP,
                self.flops_ui_ip,
                get_mlflow_tracking_server_url(),
                str(training_conf.training_rounds),
                str(training_conf.min_available_clients),
                str(training_conf.min_fit_clients),
                str(training_conf.min_evaluate_clients),
            )
        )

        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                app_id=self.flops_project_id,
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(
                    app_name=self.flops_project.app_name,
                    app_namespace=self.flops_project.namespace,
                    service_name=f"aggr{get_shortened_id(self.flops_project.flops_project_id)}",
                    service_namespace=self.namespace,
                ),
                compute=SlaCompute(
                    code=self.fl_aggregator_image,
                    one_shot_service=True,
                    cmd=cmd,
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
