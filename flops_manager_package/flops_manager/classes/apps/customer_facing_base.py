import abc

from flops_manager.classes.apps.app_base import FLOpsApp
from flops_manager.database.common import retrieve_from_db_by_customer_id
from flops_manager.utils.sla.components import SlaComponentsWrapper, SlaCore, SlaNames
from pydantic import AliasChoices, Field


class FLOpsCustomerFacingApp(FLOpsApp, abc.ABC):
    namespace = "customerfacingapp"

    customer_id: str = Field(alias=AliasChoices("customer_id", "customerID"))

    def _configure_sla_components(self) -> None:
        self.sla_components = SlaComponentsWrapper(
            core=SlaCore(
                customerID=self.customer_id,
                names=SlaNames(
                    # TODO investigate if this can lead to name collisions
                    # keep in mind: 1 observer for 1 user - so we could be fine
                    app_name=self.namespace,
                    app_namespace=self.namespace,
                ),
            ),
        )

    @classmethod
    def get_app(cls, customer_id: str) -> "FLOpsCustomerFacingApp":
        """There should be only one per user."""
        existing_app = retrieve_from_db_by_customer_id(cls, customer_id)
        return existing_app or cls(customer_id=customer_id)
