from flops_manager.classes.apps.observatory.main import FLOpsObservatory
from flops_manager.database.common import retrieve_from_db_by_customer_id


def get_observatory(customer_id: str) -> FLOpsObservatory:
    existing_observatory = retrieve_from_db_by_customer_id(FLOpsObservatory, customer_id)
    return existing_observatory or FLOpsObservatory(customer_id=customer_id)
