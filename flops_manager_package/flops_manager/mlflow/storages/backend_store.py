from contextlib import contextmanager

import pymysql
from flops_manager.mlflow.storages.common import get_user_store_name
from flops_manager.utils.env_vars import BACKEND_STORE_IP
from flops_utils.logging import colorful_logger as logger

# NOTE/Future Work:
# Currently the Tracking Server is used as a proxy for both stores,
# thus only a single user/account is enough for it to work.
# However, hardcoding the access like this is not good regarding security.
# This access control/isolation can be further enhanced.
# E.g. by the uses of dedicated user accounts for each customer.
# Right now the content and access is isolated by creating sub-folders for each client.

BACKEND_STORE_PORT = 3306
BACKEND_STORE_CONNECTION_USER_NAME = "root"
BACKEND_STORE_CONNECTION_PWD = "oakestra"


def get_user_backend_store_uri(customer_id: str) -> str:
    return "".join(
        (
            "mysql+pymysql",
            "://",
            BACKEND_STORE_CONNECTION_USER_NAME,
            ":",
            BACKEND_STORE_CONNECTION_PWD,
            "@",
            BACKEND_STORE_IP,
            ":",
            str(BACKEND_STORE_PORT),
            "/",
            get_user_store_name(customer_id),
        )
    )


@contextmanager
def _get_db_connection():
    connection = pymysql.connect(
        host=BACKEND_STORE_IP,
        user=BACKEND_STORE_CONNECTION_USER_NAME,
        password=BACKEND_STORE_CONNECTION_PWD,
        port=BACKEND_STORE_PORT,
    )
    try:
        yield connection
    finally:
        connection.close()


def ensure_user_backend_store_exists(customer_id: str) -> None:
    db_name = get_user_store_name(customer_id)
    with _get_db_connection() as db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
            result = cursor.fetchone()
            if not result:
                cursor.execute(f"CREATE DATABASE {db_name}")
                logger.info(f"Backend Store Database for '{db_name}' created.")
