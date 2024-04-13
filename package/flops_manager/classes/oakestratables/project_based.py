from abc import ABC

from flops_manager.api.app_management import create_app
from flops_manager.classes.oakestratables.base import FlOpsOakestraBaseClass
from flops_manager.classes.project_based import FlOpsProjectBasedClass
from flops_manager.utils.sla.generator import generate_sla
from flops_manager.utils.types import Application


class FlOpsOakestraProjectBasedClass(FlOpsOakestraBaseClass, FlOpsProjectBasedClass, ABC):

    def create(self) -> Application:
        return create_app(
            sla=generate_sla(self.sla_components),
            bearer_token=getattr(self, "bearer_token", None),
            flops_project_id=self.flops_project_id,
            matching_caller_object=self,
        )
