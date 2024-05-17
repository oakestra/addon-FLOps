from flops_manager.mlflow.storages.backend_store import ensure_user_backend_store_exists


def handle_storages(customer_id: str) -> None:
    """A Tracking Server is a proxy for persistent data stores.

    There are two different ones.
    - (A) The Artifact Store / Model Registry for larger objects like model weights.
    - (B) The Backend Store for (lightweight) metadata like metrics.

    Each User should have his own private/isolated piece of storage.
    For (B) we provide each user with his own database.
    """

    ensure_user_backend_store_exists(customer_id)
