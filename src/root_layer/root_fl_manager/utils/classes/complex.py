from abc import ABC
from dataclasses import dataclass, field

from api.utils import create_app, deploy_service, fetch_app, undeploy_app
from flops.process import FlOpsProcess
from utils.classes.base import FlOpsBaseClass
from utils.types import Application, AppSLA


@dataclass
class FlOpsDeployableClass(FlOpsBaseClass, ABC):
    flops_process_id: str

    app_id: str = field(init=False, default="")
    service_id: str = field(init=False, default="")

    def __init__(self, flops_process_id: str):
        super().__init__(flops_process_id=flops_process_id)

    def __post_init__(self):
        deploy_service(service_id=self.service_id, matching_caller_object=self)
        self._add_to_db()

    def _create(
        self, flops_process: FlOpsProcess, app_sla: AppSLA, bearer_token: str = None
    ) -> None:
        new_app = create_app(
            sla=app_sla,
            bearer_token=bearer_token,
            flops_process=flops_process,
            matching_caller_object=self,
        )
        self.app_id = new_app["applicationID"]
        self.service_id = new_app["microservices"][-1]

    def fetch_app(self, app_namespace: str) -> Application:
        return fetch_app(
            app_namespace=app_namespace,
            flops_process_id=self.flops_process_id,
            matching_caller_object=self,
        )

    def undeploy_app(self) -> None:
        undeploy_app(
            application_id=self.app_id,
            flops_process_id=self.flops_process_id,
            matching_caller_object=self,
        )
