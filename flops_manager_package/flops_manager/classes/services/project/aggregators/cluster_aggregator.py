import hashlib

from flops_manager.classes.services.project.aggregators.classic_aggregator import (
    ClassicFLAggregator,
)
from flops_manager.utils.common import generate_ip, get_shortened_unique_id
from flops_manager.utils.constants import FLOPS_USER_ACCOUNT
from flops_manager.utils.env_vars import FLOPS_MQTT_BROKER_IP
from flops_manager.utils.sla.components import (
    ClusterConstraint,
    SlaComponentsWrapper,
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
)
from flops_utils.types import AggregatorType
from pydantic import Field


class ClusterFLAggregator(ClassicFLAggregator):
    namespace = "raggr"

    root_fl_aggregator_ip: str = Field(default="", exclude=True, repr=False)
    cluster_name: str
    cluster_id: str

    def generate_unique_ip(self) -> str:
        unique_id = hashlib.sha256(
            (self.parent_app.flops_project_id + self.cluster_id).encode()  # type: ignore
        ).hexdigest()[: len(self.cluster_id)]
        return generate_ip(unique_id=unique_id, object=self)

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
                AggregatorType.CLUSTER_AGGREGATOR.value,
                str(training_conf.training_rounds),
                str(training_conf.min_available_clients),
                str(training_conf.min_fit_clients),
                str(training_conf.min_evaluate_clients),
                self.root_fl_aggregator_ip,
            )
        )
        unique_name = "cag" + get_shortened_unique_id(self.cluster_id + self.flops_project_id)
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                app_id=self.flops_project_id,
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(
                    app_name=self.parent_app.app_name,  # type: ignore
                    app_namespace=self.parent_app.namespace,  # type: ignore
                    service_name=unique_name,
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
                constraints=[ClusterConstraint(allowed=[self.cluster_name])],
            ),
        )
