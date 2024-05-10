from flops_manager.classes.apps.app_base import FLOpsApp
from flops_manager.database.common import retrieve_from_db_by_customer_id
from flops_manager.utils.sla.components import SlaComponentsWrapper, SlaCore, SlaNames
from pydantic import AliasChoices, Field


class FLOpsObservatory(FLOpsApp):
    """A user-facing app that hosts services for observing the current FLOps project(s)
    as well as legacy ones."""

    namespace = "observatory"
    customer_id: str = Field(alias=AliasChoices("customer_id", "customerID"))

    def _configure_sla_components(self) -> None:
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=self.customer_id,
                names=SlaNames(
                    # TODO investigate if this can lead to name collisions
                    # keep in mind: 1 observ for 1 user - so we could be fine
                    app_name=self.namespace,
                    app_namespace=self.namespace,
                ),
            ),
        )


def get_observatory(customer_id: str) -> FLOpsObservatory:
    """There should be only one observatory per user."""
    existing_observatory = retrieve_from_db_by_customer_id(FLOpsObservatory, customer_id)
    return existing_observatory or FLOpsObservatory(customer_id=customer_id)
