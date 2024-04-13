from abc import abstractmethod
from typing import ClassVar

from flops_manager.api.app_management import create_app, fetch_app
from flops_manager.classes.base import FlOpsBaseClass
from flops_manager.utils.sla.components import SlaComponentsWrapper
from flops_manager.utils.sla.generator import generate_sla
from flops_manager.utils.types import Application
from pydantic import Field


class FlOpsOakestraBaseClass(FlOpsBaseClass):
    """A class used for components that can be created or deployed as applications or services."""

    # Note:
    # This "Field"s help to make the constructor call for human developers easier to read.
    # It removes fields that should not be explicitly displayed in the IDE hints.
    # This does not break loading/reinstantiating the object when fetching it from the DB.
    #
    # The only downside is that it still requires a set value during the constructor call.
    # The current workaround is to set a dummy default value.
    # The potential issue here is that if this field is not set correctly during the construction,
    # this object will still count as valid, which it is not.
    #
    # TODO add a "post init" (custom) validator to check
    # if all properties are properly set and not empty/""
    namespace: ClassVar[str]
    # Note: Only used during "runtime". It is not stored or displayed due to verbosity & redundancy.
    sla_components: SlaComponentsWrapper = Field(None, init=False, exclude=True, repr=False)

    app_id: str = Field("", init=False)
    app_name: str = Field("", init=False)

    def model_post_init(self, _) -> None:
        if self.gets_loaded_from_db:
            return

        self._configure_sla_components()
        created_app = self.create()
        self._set_properties_based_on_created_app(created_app)
        self._add_to_db()

    @abstractmethod
    def _configure_sla_components(self) -> None:
        """Sets self.sla_components that are needed for deployments"""
        pass

    def create(self) -> Application:
        return create_app(
            sla=generate_sla(self.sla_components),
            matching_caller_object=self,
        )

    def _set_properties_based_on_created_app(self, created_app: Application) -> None:
        self.app_id = created_app["applicationID"]
        self.app_name = created_app["application_name"]
        if created_app["microservices"]:
            self.service_id = created_app["microservices"][-1]

    def fetch_from_oakestra(self) -> Application:
        return fetch_app(
            app_id=self.app_id,
            matching_caller_object=self,
        )
