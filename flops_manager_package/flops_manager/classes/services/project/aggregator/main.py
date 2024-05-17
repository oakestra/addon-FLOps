from flops_manager.classes.services.project.project_service import FLOpsProjectService
from flops_manager.image_management import FLOpsImageTypes, get_flops_image_name
from flops_manager.mqtt.sender import notify_project_observer
from flops_manager.utils.common import generate_ip, get_shortened_unique_id
from flops_manager.utils.constants import FLOPS_USER_ACCOUNT
from flops_manager.utils.env_vars import FLOPS_MQTT_BROKER_IP
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
    namespace = "aggr"
    fl_aggregator_image: str = Field("", init=False)
    project_observer_ip: str = Field("", exclude=True, repr=False)
    tracking_server_url: str = Field("", exclude=True, repr=False)

    ip: str = Field("", init=False)

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        if self.parent_app.verbose:
            notify_project_observer(
                flops_project_id=self.parent_app.flops_project_id,
                msg="Preparing new FL Aggregator.",
            )

        self.ip = generate_ip(self.parent_app.flops_project_id, self)
        self.fl_aggregator_image = get_flops_image_name(
            ml_repo_url=self.parent_app.ml_repo_url,
            ml_repo_latest_commit_hash=self.parent_app.ml_repo_latest_commit_hash,
            flops_image_type=FLOpsImageTypes.AGGREGATOR,
        )
        super().model_post_init(_)

        if self.parent_app.verbose:
            notify_project_observer(
                flops_project_id=self.parent_app.flops_project_id,
                msg="New Aggregator service created & deployed",
            )

    def _configure_sla_components(self) -> None:
        training_conf = self.parent_app.training_configuration

        cmd = " ".join(
            (
                "python",
                "main.py",
                self.flops_project_id,
                FLOPS_MQTT_BROKER_IP,
                self.project_observer_ip,
                self.tracking_server_url,
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
                    app_name=self.parent_app.app_name,
                    app_namespace=self.parent_app.namespace,
                    service_name=f"aggr{get_shortened_unique_id(self.flops_project_id)}",
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
