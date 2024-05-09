from flops_manager.classes.application import FLOpsApp
from flops_manager.utils.sla.components import SlaComponentsWrapper, SlaCore, SlaDetails, SlaNames
from pydantic import AliasChoices, Field


class FLOpsObservatory(FLOpsApp):
    """A user-facing app that hosts services for observing the current FLOps project(s)
    as well as legacy ones."""

    customer_id: str = Field(alias=AliasChoices("customer_id", "customerID"))

    namespace = "flopsobservatory"

    def build_sla_components(self) -> SlaComponentsWrapper:
        return SlaComponentsWrapper(
            core=SlaCore(
                customerID=self.customer_id,
                names=SlaNames(
                    # TODO investigate if this can lead to name collisions
                    # keep in mind: 1 observ for 1 user - so we could be fine
                    app_name=self.namespace,
                    app_namespace=self.namespace,
                ),
            ),
            details=SlaDetails(app_desc="TODO"),
        )
