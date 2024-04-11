from flops_manager.flops.classes.abstract.internal_component import InternalProjectComponent
from flops_manager.flops.classes.aggregator.sla import prepare_aggregator_sla_components
from flops_manager.flops.classes.project import FlOpsProject
from flops_manager.flops.classes.ui import UserInterface
from pydantic import Field


class FLAggregator(InternalProjectComponent):
    flops_project: FlOpsProject = Field(None, exclude=True, repr=False)
    ui: UserInterface = Field(None, exclude=True, repr=False)

    ip: str = Field("", init=False)

    flops_project_id: str = Field("", init=False)

    namespace = "flaggreg"

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        self.flops_project_id = self.flops_project.flops_project_id
        super().model_post_init(_)

    def _configure_sla_components(self) -> None:
        self.sla_components = prepare_aggregator_sla_components(self)
