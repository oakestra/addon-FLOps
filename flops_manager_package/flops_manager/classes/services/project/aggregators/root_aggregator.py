from flops_manager.classes.services.project.aggregators.classic_aggregator import (
    ClassicFLAggregator,
)
from flops_manager.classes.services.project.aggregators.cluster_aggregator import (
    ClusterFLAggregator,
)
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_manager.utils.common import get_shortened_unique_id
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


class RootFLAggregator(ClassicFLAggregator):
    namespace = "raggr"

    number_of_cluster_aggregators: int

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

    # TODO/FUTURE WORK: Refactor the two methods a bit to reduce code duplication.
    @classmethod
    def handle_aggregator_failed(cls, aggregator_failed_msg: dict) -> None:
        flops_project_id = aggregator_failed_msg["flops_project_id"]
        cluster_aggregator = retrieve_from_db_by_project_id(ClusterFLAggregator, flops_project_id)
        cluster_aggregator.undeploy()  # type: ignore
        super().handle_aggregator_failed(aggregator_failed_msg)

    @classmethod
    def handle_aggregator_success(cls, aggregator_success_msg: dict) -> None:
        flops_project_id = aggregator_success_msg["flops_project_id"]
        cluster_aggregator = retrieve_from_db_by_project_id(ClusterFLAggregator, flops_project_id)
        cluster_aggregator.undeploy()  # type: ignore
        super().handle_aggregator_success(aggregator_success_msg)
