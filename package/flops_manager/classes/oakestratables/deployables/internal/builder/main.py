from flops_manager.classes.ml_repo import MlRepo
from flops_manager.classes.oakestratables.deployables.internal.base import InternalProjectComponent
from flops_manager.classes.oakestratables.deployables.internal.builder.sla import (
    prepare_builder_sla_components,
)
from flops_manager.classes.oakestratables.deployables.public.ui import UserInterface
from flops_manager.classes.oakestratables.project import FlOpsProject
from pydantic import Field


class FLClientEnvImageBuilder(InternalProjectComponent):
    flops_project: FlOpsProject = Field(None, exclude=True, repr=False)
    ui: UserInterface = Field(None, exclude=True, repr=False)
    ml_repo: MlRepo = Field(None, exclude=True, repr=False)

    flops_project_id: str = Field("", init=False)

    namespace = "flbuild"

    def model_post_init(self, _):
        if self.gets_loaded_from_db:
            return

        self.flops_project_id = self.flops_project.flops_project_id
        super().model_post_init(_)

    def _configure_sla_components(self) -> None:
        self.sla_components = prepare_builder_sla_components(self)
