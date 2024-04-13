from abc import ABC

from flops_manager.api.service_management import append_service_to_flops_project_app
from flops_manager.classes.oakestratables.deployables.project_based import (
    DeployableProjectBasedClass,
)
from flops_manager.utils.sla.generator import generate_sla


class FLOpsProjectService(DeployableProjectBasedClass, ABC):
    """Such a service will be appended to an already existing FLOps project application."""

    def model_post_init(self, _) -> None:
        if self.gets_loaded_from_db:
            return

        self._configure_sla_components()
        self.create()
        self._add_to_db()
        self.deploy()

    def create(self) -> None:
        self.service_id = append_service_to_flops_project_app(
            sla=generate_sla(self.sla_components),
            bearer_token=getattr(self, "bearer_token", None),
            flops_project_id=self.flops_project_id,
            matching_caller_object=self,
        )
