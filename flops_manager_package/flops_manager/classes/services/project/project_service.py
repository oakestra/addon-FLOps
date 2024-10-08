from abc import ABC
from typing import Optional

from flops_manager.classes.apps.project import FLOpsProject
from flops_manager.classes.services.service_base import FLOpsService
from pydantic import Field


class FLOpsProjectService(FLOpsService, ABC):
    parent_app: Optional[FLOpsProject] = Field(default=None, exclude=True, repr=False)
    flops_project_id: str = Field("", init=False)

    def model_post_init(self, _) -> None:
        if self.gets_loaded_from_db:
            return

        self.flops_project_id = self.parent_app.flops_project_id  # type: ignore
        super().model_post_init(_)
