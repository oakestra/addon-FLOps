from http import HTTPStatus
from typing import Tuple

import flask
import flask_openapi3
from flops_manager.database.main import reset_db
from flops_manager.utils.exceptions.main import FLOpsManagerException
from flops_utils.logging import colorful_logger as logger

database_blp = flask_openapi3.APIBlueprint(
    "database",
    __name__,
    url_prefix="/api/flops/database",
)


@database_blp.delete("/")
def reset_database() -> Tuple[dict, HTTPStatus]:
    try:
        customer_id = flask.request.json["customerID"]  # type: ignore
        if customer_id != "Admin":
            return {
                "message": "Only Admins are allowed to reset the database!"
            }, HTTPStatus.FORBIDDEN
        reset_db()
    except FLOpsManagerException as e:
        e.log()
        return {"message": e.message}, e.http_status or HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        err_msg = "Unexpected exception occurred"
        logger.exception(err_msg)
        return {"message": f"{err_msg}:{e}"}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {"message": "Successfully reset the database."}, HTTPStatus.OK
