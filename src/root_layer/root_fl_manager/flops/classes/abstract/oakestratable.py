from abc import abstractmethod
from typing import ClassVar

from api.app_management import create_app, fetch_app
from flops.classes.abstract.base import FlOpsBaseClass
from icecream import ic
from pydantic import Field
from utils.sla.components import SlaComponentsWrapper
from utils.sla.generator import generate_sla
from utils.types import Application


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

    def model_post_init(self, _) -> None:
        if self.gets_loaded_from_db:
            return

        ic(0)
        self._configure_sla_components()
        ic(1, self.sla_components)
        self.create()
        ic(2)
        self._add_to_db()
        ic(3)

    @abstractmethod
    def _configure_sla_components(self) -> None:
        """Sets self.sla_components that are needed for deployments"""
        pass

    def create(self) -> None:
        ic(4)
        sla = generate_sla(self.sla_components)
        ic(sla)
        ic("4aa")

        new_app = create_app(
            # sla=generate_sla(self.sla_components),
            sla=sla,
            bearer_token=getattr(self, "bearer_token", None),
            flops_project_id=self.flops_project_id,
            matching_caller_object=self,
        )
        ic(5, self.flops_project_id, new_app)
        if self.flops_project_id:
            self.app_id = new_app["applicationID"]
            ic(55, self.app_id)
        else:
            self.flops_project_id = new_app["applicationID"]
        if new_app["microservices"]:
            self.service_id = new_app["microservices"][-1]
            ic(555, self.service_id)

        ic(6)

    def delete(self) -> None:
        pass
        # TODO
        # delete_app(
        #     application_id=self.app_id,
        #     flops_project_id=self.flops_project_id,
        #     matching_caller_object=self,
        # )

    def fetch_from_oakestra(self, namespace: str) -> Application:
        return fetch_app(
            app_namespace=namespace,
            flops_project_id=self.flops_project_id,
            matching_caller_object=self,
        )
