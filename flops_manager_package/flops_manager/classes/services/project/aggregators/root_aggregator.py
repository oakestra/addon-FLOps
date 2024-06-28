from flops_manager.classes.services.project.aggregators.classic_aggregator import FLAggregator
from flops_manager.image_management.fl_actor_images import (
    FLActorImageTypes,
    get_fl_actor_image_name,
)
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
from flops_utils.types import AggregatorType


class RootFLAggregator(FLAggregator):
    namespace = "raggr"

    number_of_cluster_aggregators: int

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        if self.parent_app.verbose:  # type: ignore
            notify_project_observer(
                flops_project_id=self.parent_app.flops_project_id,  # type: ignore
                msg="Preparing new Root FL Aggregator.",
            )

        self.ip = generate_ip(
            self.parent_app.flops_project_id,  # type: ignore
            self,
        )
        self.fl_aggregator_image = get_fl_actor_image_name(
            ml_repo_url=self.parent_app.ml_repo_url,  # type: ignore
            ml_repo_latest_commit_hash=self.parent_app.ml_repo_latest_commit_hash,  # type: ignore
            flops_image_type=FLActorImageTypes.AGGREGATOR,
        )
        super().model_post_init(_)

        if self.parent_app.verbose:  # type: ignore
            notify_project_observer(
                flops_project_id=self.parent_app.flops_project_id,  # type: ignore
                msg="New Root Aggregator service created & deployed",
            )

    def _configure_sla_components(self) -> None:
        training_conf = self.parent_app.training_configuration  # type: ignore

        cmd = " ".join(
            (
                "python",
                "main.py",
                self.flops_project_id,
                FLOPS_MQTT_BROKER_IP,
                self.project_observer_ip,
                self.tracking_server_url,
                AggregatorType.ROOT_AGGREGATOR.value,
                str(training_conf.training_cycles),
                # NOTE:
                # Min. number of available clients, etc. - in this case cluster aggregators.
                # Currently we assume that the number of active clusters stays the same.
                # Future work can introduce more flexible and error-prone solutions.
                str(self.number_of_cluster_aggregators),
                str(self.number_of_cluster_aggregators),
                str(self.number_of_cluster_aggregators),
            )
        )

        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                app_id=self.flops_project_id,
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(
                    app_name=self.parent_app.app_name,  # type: ignore
                    app_namespace=self.parent_app.namespace,  # type: ignore
                    service_name=f"raggr{get_shortened_unique_id(self.flops_project_id)}",
                    service_namespace=self.namespace,
                ),
                compute=SlaCompute(
                    code=self.fl_aggregator_image,
                    one_shot_service=True,
                    cmd=cmd,
                ),
            ),
            details=SlaDetails(
                rr_ip=self.ip,  # type: ignore
                resources=SlaResources(
                    memory=100,
                    vcpus=1,
                    storage=0,
                ),
            ),
        )
