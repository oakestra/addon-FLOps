from flops_manager.classes.oak.project_based import FlOpsOakestraProjectBasedClass
from flops_manager.utils.sla.components import SlaComponentsWrapper, SlaCore, SlaDetails, SlaNames


class FLOpsObservatory(FlOpsOakestraProjectBasedClass):
    """Links all FL and ML/DevOps observation components related to one FLOps project.
    These components are user-facing"""

    namespace = "flopsobserv"

    def _configure_sla_components(self) -> None:
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=self.flops_project.customer_id,
                names=SlaNames(
                    app_name=f"flopsobserv{self.flops_project.get_shortened_id()}",
                    app_namespace=self.namespace,
                ),
            ),
            details=SlaDetails(app_desc="User facing application for observing a FLOps project"),
        )
