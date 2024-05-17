from flops_manager.mlflow.storages.common import get_user_store_name
from flops_manager.utils.env_vars import ARTIFACT_STORE_IP

# Note/Future Work:
# Currently the Tracking Server is used as a proxy for both stores,
# thus only a single user/account is enough for it to work.
# However, hardcoding the access like this is not good regarding security.
# This access control/isolation can be further enhanced.
# E.g. by the uses of dedicated user accounts for each customer.
# Right now the content and access is isolated by creating sub-folders for each client.

ARTIFACT_STORE_CONNECTION_USER_NAME = "flops"
ARTIFACT_STORE_CONNECTION_PWD = "flops"


def get_user_artifact_store_uri(customer_id: str) -> str:
    return "".join(
        (
            "ftp",
            "://",
            ARTIFACT_STORE_CONNECTION_USER_NAME,
            ":",
            ARTIFACT_STORE_CONNECTION_PWD,
            "@",
            ARTIFACT_STORE_IP,
            "/flops_artifacts/",
            get_user_store_name(customer_id),
        )
    )
