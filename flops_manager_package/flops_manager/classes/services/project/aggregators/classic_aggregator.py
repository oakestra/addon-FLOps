from flops_manager.classes.apps.project import FLOpsProject
from flops_manager.classes.services.project.learners.main import FLLearners
from flops_manager.classes.services.project.project_service import FLOpsProjectService
from flops_manager.database.common import retrieve_from_db_by_project_id
from flops_manager.flops_management.post_training_steps.build_trained_model_image import (
    init_fl_post_training_steps,
)
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
from flops_utils.logging import colorful_logger as logger
from flops_utils.types import AggregatorType
from pydantic import Field


class ClassicFLAggregator(FLOpsProjectService):
    namespace = "aggr"
    fl_aggregator_image: str = Field("", init=False)
    project_observer_ip: str = Field("", exclude=True, repr=False)
    tracking_server_url: str = Field("", exclude=True, repr=False)

    ip: str = Field("", init=False)

    def generate_unique_ip(self) -> str:
        return generate_ip(self.parent_app.flops_project_id, self)  # type: ignore

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        if self.parent_app.verbose:  # type: ignore
            notify_project_observer(
                flops_project_id=self.parent_app.flops_project_id,  # type: ignore
                msg="Preparing new FL Aggregator.",
            )

        self.ip = self.generate_unique_ip()
        self.fl_aggregator_image = get_fl_actor_image_name(
            ml_repo_url=self.parent_app.ml_repo_url,  # type: ignore
            ml_repo_latest_commit_hash=self.parent_app.ml_repo_latest_commit_hash,  # type: ignore
            flops_image_type=FLActorImageTypes.AGGREGATOR,
        )
        super().model_post_init(_)

        if self.parent_app.verbose:  # type: ignore
            notify_project_observer(
                flops_project_id=self.parent_app.flops_project_id,  # type: ignore
                msg="New Aggregator service created & deployed",
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
                AggregatorType.CLASSIC_AGGREGATOR.value,
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
                    app_name=self.parent_app.app_name,  # type: ignore
                    app_namespace=self.parent_app.namespace,  # type: ignore
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
        logger.debug(aggregator_failed_msg)
        flops_project_id = aggregator_failed_msg["flops_project_id"]
        retrieve_from_db_by_project_id(cls, flops_project_id).undeploy()  # type: ignore
        retrieve_from_db_by_project_id(FLLearners, flops_project_id).undeploy()  # type: ignore
        msg = f"{cls.__name__} failed. Terminating this FLOps Project."
        logger.critical(msg)
        notify_project_observer(flops_project_id=flops_project_id, msg=msg)

    @classmethod
    def handle_aggregator_success(cls, aggregator_success_msg: dict) -> None:
        logger.debug("Aggregator successfully finished training.")
        flops_project_id = aggregator_success_msg["flops_project_id"]
        retrieve_from_db_by_project_id(cls, flops_project_id).undeploy()  # type: ignore
        retrieve_from_db_by_project_id(FLLearners, flops_project_id).undeploy()  # type: ignore
        init_fl_post_training_steps(
            flops_project=retrieve_from_db_by_project_id(
                FLOpsProject,  # type: ignore
                flops_project_id,  # type: ignore
            ),
            winner_model_run_id=aggregator_success_msg["run_id"],
        )
