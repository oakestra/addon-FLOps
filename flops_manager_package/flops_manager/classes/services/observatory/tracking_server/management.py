from flops_manager.classes.apps.observatory import FLOpsObservatory, get_observatory
from flops_manager.classes.services.observatory.tracking_server.main import TrackingServer
from flops_manager.database.common import retrieve_from_db_by_customer_id
from flops_manager.mlflow.storages.main import handle_storages


def get_tracking_server(customer_id: str, observatory: FLOpsObservatory = None) -> TrackingServer:
    """There should only be one tracking server per user."""
    existing_tracking_server = retrieve_from_db_by_customer_id(TrackingServer, customer_id)
    if existing_tracking_server:
        return existing_tracking_server

    if not observatory:
        observatory = get_observatory(customer_id)
    handle_storages(customer_id)
    return TrackingServer(parent_app=observatory, customer_id=customer_id)
