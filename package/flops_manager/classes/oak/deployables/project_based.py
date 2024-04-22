from abc import ABC

from flops_manager.api.service_management import undeploy
from flops_manager.classes.oak.deployables.base import DeployableClass
from flops_manager.classes.oak.project_based import FlOpsOakestraProjectBasedClass


class DeployableProjectBasedClass(DeployableClass, FlOpsOakestraProjectBasedClass, ABC):

    def undeploy(self) -> None:
        undeploy(
            service_id=self.service_id,
            matching_caller_object=self,
            flops_project_id=self.flops_project_id,
        )
        self.remove_from_db()
