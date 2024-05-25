from flops_manager.classes.apps.customer_facing_base import FLOpsCustomerFacingApp


class FLOpsHelperApp(FLOpsCustomerFacingApp):
    """A customer-facing wrapper app for hosting optional auxiliary FLOps services.

    E.g. hosts mock-data-providers.
    """

    namespace = "helper"
