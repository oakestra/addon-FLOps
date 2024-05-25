from flops_manager.classes.apps.customer_facing_base import FLOpsCustomerFacingApp


class FLOpsObservatory(FLOpsCustomerFacingApp):
    """A user-facing app that hosts services for observing the current FLOps project(s)
    as well as legacy ones."""

    namespace = "observatory"
