from abc import ABC, abstractmethod

from api.utils import create_app, deploy_service, fetch_app, undeploy
from flops.classes.abstract.base import FlOpsBaseClass
from flops.classes.process import FlOpsProcess
from pydantic import Field
from utils.sla.components import SlaComponentsWrapper
from utils.sla.generator import generate_sla
from utils.types import Application


class FlOpsDeployableClass(FlOpsBaseClass, ABC):
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
    app_id: str = Field("", init=False)
    service_id: str = Field("", init=False)

    # Note: Only used during "runtime". It is not stored or displayed due to verbosity & redundancy.
    sla_components: SlaComponentsWrapper = Field(None, init=False, exclude=True, repr=False)

    def model_post_init(self, _) -> None:
        self._configure_sla_components()

    @abstractmethod
    def _configure_sla_components(self) -> None:
        """Sets self.sla_components that are needed for deployments"""
        pass

    def deploy(self, bearer_token: str = None) -> None:
        new_app = create_app(
            sla=generate_sla(self.sla_components),
            bearer_token=bearer_token,
            flops_process_id=self.flops_process_id,
            matching_caller_object=self,
        )
        self.app_id = new_app["applicationID"]
        self.service_id = new_app["microservices"][-1]
        deploy_service(service_id=self.service_id, matching_caller_object=self)
        self._add_to_db()

    def undeploy(self) -> None:
        undeploy(
            application_id=self.app_id,
            flops_process_id=self.flops_process_id,
            matching_caller_object=self,
        )

    def fetch_from_oakestra(self, namespace: str) -> Application:
        return fetch_app(
            app_namespace=namespace,
            flops_process_id=self.flops_process_id,
            matching_caller_object=self,
        )
