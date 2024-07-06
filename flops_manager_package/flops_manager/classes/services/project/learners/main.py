from flops_manager.api.service_management import deploy
from flops_manager.classes.services.project.project_service import FLOpsProjectService
from flops_manager.image_management.fl_actor_images import (
    FLActorImageTypes,
    get_fl_actor_image_name,
)
from flops_manager.mqtt.sender import notify_project_observer
from flops_manager.utils.common import get_shortened_unique_id
from flops_manager.utils.constants import FLOPS_USER_ACCOUNT
from flops_manager.utils.env_vars import FLOPS_MQTT_BROKER_IP
from flops_manager.utils.sla.components import (
    FLOPS_LEARNER_ADDON_TYPE,
    AddonConstraint,
    ClusterConstraint,
    SlaComponentsWrapper,
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
)
from pydantic import Field


class FLLearners(FLOpsProjectService):
    namespace = "flearner"

    project_observer_ip: str = Field("", exclude=True, repr=False)
    tracking_server_url: str = Field("", exclude=True, repr=False)

    number_of_learners: int = Field(1, init=False)
    fl_learner_image: str = Field("", init=False)
    fl_aggregator_ip: str = Field(default="", exclude=True, repr=False)

    cluster_name: str = ""
    cluster_id: str = ""

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        if self.parent_app.verbose:  # type: ignore
            notify_project_observer(
                flops_project_id=self.parent_app.flops_project_id,  # type: ignore
                msg="Preparing new FL Learners.",
            )

        self.number_of_learners = (
            self.parent_app.training_configuration.min_available_clients  # type: ignore
        )
        self.fl_learner_image = get_fl_actor_image_name(
            ml_repo_url=self.parent_app.ml_repo_url,  # type: ignore
            ml_repo_latest_commit_hash=self.parent_app.ml_repo_latest_commit_hash,  # type: ignore
            flops_image_type=FLActorImageTypes.LEARNER,
        )
        super().model_post_init(_)

        if self.parent_app.verbose:  # type: ignore
            notify_project_observer(
                flops_project_id=self.parent_app.flops_project_id,  # type: ignore
                msg="New FL Learners service created & deployed",
            )

    def deploy(self) -> None:
        for _ in range(self.number_of_learners):
            deploy(service_id=self.service_id, matching_caller_object=self)

    def _configure_sla_components(self) -> None:
        data_tags = self.parent_app.training_configuration.data_tags  # type: ignore
        f"python main.py {self.fl_aggregator_ip} {data_tags}"
        cmd = " ".join(
            (
                "python",
                "main.py",
                self.flops_project_id,
                FLOPS_MQTT_BROKER_IP,
                self.project_observer_ip,
                str(self.fl_aggregator_ip),
                # NOTE: This turns the tag list into a single comma-separated string.
                ",".join(self.parent_app.training_configuration.data_tags),  # type: ignore
            )
        )
        flops_project_id = self.parent_app.flops_project_id  # type: ignore
        unique_id = flops_project_id
        if self.cluster_id:
            unique_id += self.cluster_id
        service_name = f"flearner{get_shortened_unique_id(unique_id)}"

        constraints = [AddonConstraint(needs=[FLOPS_LEARNER_ADDON_TYPE])]
        if self.cluster_name:
            constraints.append(ClusterConstraint(allowed=[self.cluster_name]))  # type: ignore

        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                app_id=self.flops_project_id,
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(
                    app_name=self.parent_app.app_name,  # type: ignore
                    app_namespace=self.parent_app.namespace,  # type: ignore
                    service_name=service_name,
                    service_namespace=self.namespace,
                ),
                compute=SlaCompute(
                    code=self.fl_learner_image,
                    one_shot_service=True,
                    cmd=cmd,
                ),
            ),
            details=SlaDetails(
                resources=SlaResources(
                    memory=100,
                    vcpus=1,
                    storage=0,
                ),
                constraints=constraints,  # type: ignore
            ),
        )
