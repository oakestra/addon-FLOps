from abc import ABC, abstractmethod

from api.utils import create_app, deploy_service, fetch_app, undeploy
from flops.process import FlOpsProcess
from utils.classes.base import FlOpsBaseClass
from utils.types import Application, AppSLA


class FlOpsDeployableClass(FlOpsBaseClass, ABC):
    app_id: str = ""
    service_id: str = ""

    @abstractmethod
    def _create_sla(self, flops_process: FlOpsProcess) -> AppSLA:
        pass

    def deploy(
        self,
        flops_process: FlOpsProcess,
        bearer_token: str = None,
    ) -> None:
        new_app = create_app(
            sla=self._create_sla(flops_process),
            bearer_token=bearer_token,
            flops_process=flops_process,
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
