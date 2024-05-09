from flops_manager.api.service_management import deploy
from flops_manager.classes.deployables.project_services.aggregator.main import FLAggregator
from flops_manager.classes.deployables.project_services.base import FLOpsProjectService
from flops_manager.image_management import FLOpsImageTypes, get_flops_image_name
from flops_manager.mqtt.sender import notify_project_observer
from flops_manager.utils.common import get_shortened_id
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


class FLLearners(FLOpsProjectService):
    total_number_of_learners: int = Field(1, init=False)

    fl_aggregator: FLAggregator = Field(None, exclude=True, repr=False)

    fl_learner_image: str = Field("", init=False)

    namespace = "flearner"

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        if self.flops_project.verbose:
            notify_project_observer(
                flops_project_id=self.flops_project_id,
                msg="Preparing new FL Learners.",
            )

        self.total_number_of_learners = (
            self.flops_project.training_configuration.min_available_clients
        )
        self.flops_project_id = self.flops_project.flops_project_id
        self.fl_learner_image = get_flops_image_name(
            ml_repo_info=self.flops_project.ml_repo_info,
            flops_image_type=FLOpsImageTypes.LEARNER,
        )
        super().model_post_init(_)

        if self.flops_project.verbose:
            notify_project_observer(
                flops_project_id=self.flops_project_id,
                msg="New FL Learners service created & deployed",
            )

    def deploy_service(self) -> None:
        for _ in range(self.total_number_of_learners):
            deploy(service_id=self.service_id, matching_caller_object=self)

    def configure_sla_components(self) -> None:
        cmd = f"python main.py {self.fl_aggregator.ip}"

        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                app_id=self.flops_project_id,
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(
                    app_name=self.flops_project.app_name,
                    app_namespace=self.flops_project.namespace,
                    service_name=f"flearner{get_shortened_id(self.flops_project.flops_project_id)}",
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
            ),
        )
