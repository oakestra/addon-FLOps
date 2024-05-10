from contextlib import contextmanager

import pymysql
from flops_utils.logging import colorful_logger as logger

BACKEND_STORE_IP = "192.168.178.44"
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
            _get_user_backend_store_name(customer_id),
        )
    )


def _get_user_backend_store_name(customer_id: str) -> str:
    # Note: Intended to be adjustable if the need arises, instead of using hardcode.
    return customer_id


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
    db_name = _get_user_backend_store_name(customer_id)
    with _get_db_connection() as db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
            result = cursor.fetchone()
            if not result:
                cursor.execute(f"CREATE DATABASE {db_name}")
                logger.info(f"Backend Store Database for '{db_name}' created.")
