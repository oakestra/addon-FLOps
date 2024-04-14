from flops_manager.classes.oakestratables.deployables.project_services.aggregator import (
    FLAggregator,
)
from flops_manager.classes.oakestratables.deployables.project_services.base import (
    FLOpsProjectService,
)
from flops_manager.classes.oakestratables.project import FlOpsProject
from flops_manager.mqtt.sender import notify_ui
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


class FLLearner(FLOpsProjectService):
    fl_learner_image: str

    flops_project: FlOpsProject = Field(None, exclude=True, repr=False)
    flops_project_id: str = Field("", init=False)
    fl_aggregator: FLAggregator = Field(exclude=True, repr=False)

    namespace = "flearner"

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        if self.flops_project.verbose:
            notify_ui(
                flops_project_id=self.flops_project_id,
                msg="Preparing new FL Learner.",
            )

        self.flops_project_id = self.flops_project.flops_project_id
        super().model_post_init(_)

        if self.flops_project.verbose:
            notify_ui(
                flops_project_id=self.flops_project_id,
                msg="New Learner service created & deployed",
            )

    def _configure_sla_components(self) -> None:
        cmd = f"python main.py {self.fl_aggregator.ip}"

        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                app_id=self.flops_project_id,
                customerID=FLOPS_USER_ACCOUNT,
                names=SlaNames(
                    app_name=self.flops_project.app_name,
                    app_namespace=self.flops_project.namespace,
                    service_name=f"fl{self.flops_project.get_shortened_id()}",
                    service_namespace=self.namespace,
                    # service_name="alex",
                    # service_namespace="alex",
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
