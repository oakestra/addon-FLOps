from abc import ABC

from flops_manager.api.app_management import create_app
from flops_manager.classes.base import FlOpsOakestraBaseClass
from flops_manager.database.common import add_to_db
from flops_manager.utils.sla.components import SlaComponentsWrapper
from flops_manager.utils.sla.generator import generate_sla
from flops_manager.utils.types import Application
from pydantic import AliasChoices, Field


class FLOpsApp(FlOpsOakestraBaseClass, ABC):
    """Represents an application in the orchestrator.
    It does not contain services from the start.
    Services can be added to such apps after creating them.
    Such an app is intended to be a place for grouping similar services."""

    app_id: str = Field("", init=False, alias=AliasChoices("app_id", "applicationID"))
    app_name: str = Field("", init=False)

    def model_post_init(self, _) -> None:
        if self.gets_loaded_from_db:
            return

        sla_components = self.build_sla_components()
        created_app = self.create_app_in_orchestrator(sla_components)
        self._set_properies_based_on_created_app(created_app)
        add_to_db(self)

    def create_app_in_orchestrator(self, sla_components: SlaComponentsWrapper) -> Application:
        return create_app(
            sla=generate_sla(sla_components),
            bearer_token=getattr(self, "bearer_token", None),
            matching_caller_object=self,
        )

    def _set_properies_based_on_created_app(self, created_app: Application) -> None:
        self.app_id = created_app["applicationID"]
        self.app_name = created_app["application_name"]
