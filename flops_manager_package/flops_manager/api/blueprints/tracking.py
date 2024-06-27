from http import HTTPStatus
from typing import Tuple

import flask
import flask_openapi3
from flops_manager.classes.services.observatory.tracking_server.management import (
    get_tracking_server,
)
from flops_manager.utils.exceptions.main import FLOpsManagerException
from flops_utils.logging import colorful_logger as logger

tracking_blp = flask_openapi3.APIBlueprint(
    "tracking",
    __name__,
    url_prefix="/api/flops/tracking",
)


@tracking_blp.get("/")
def get_tracking() -> Tuple[dict, HTTPStatus]:
    try:
        customer_id = flask.request.json["customerID"]  # type: ignore
        tracking_server_url = get_tracking_server(customer_id).get_url()
    except FLOpsManagerException as e:
        e.log()
        return {"message": e.message}, e.http_status or HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        err_msg = "Unexpected exception occurred"
        logger.exception(err_msg)
        return {"message": f"{err_msg}:{e}"}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {"tracking_server_url": tracking_server_url}, HTTPStatus.OK
