from abc import ABC

from flops_manager.api.service_management import append_service_to_flops_project_app
from flops_manager.classes.oak.deployables.base import DeployableClass
from flops_manager.database.common import add_to_db
from flops_manager.utils.sla.generator import generate_sla
from pydantic import Field


class FLOpsProjectService(DeployableClass, ABC):
    """Such a service will be appended to an already existing FLOps project application."""

    # These values are always pointing to the parent FLOps Project Application.
    # Which can be deducted by the Project ID alone.
    app_id: str = Field("", init=False, exclude=True, repr=False)
    app_name: str = Field("", init=False, exclude=True, repr=False)

    def model_post_init(self, _) -> None:
        if self.gets_loaded_from_db:
            return

        self._configure_sla_components()
        self.create()
        add_to_db(self)
        self.deploy()

    def create(self) -> None:
        self.service_id = append_service_to_flops_project_app(
            sla=generate_sla(self.sla_components),
            bearer_token=getattr(self, "bearer_token", None),
            flops_project_id=self.flops_project_id,
            matching_caller_object=self,
        )
