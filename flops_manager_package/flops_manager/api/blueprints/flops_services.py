from http import HTTPStatus
from typing import Tuple

import flask
import flask_openapi3
from flops_manager.manage_flops import handle_new_flops_project
from flops_manager.mqtt.sender import notify_ui
from flops_manager.utils.exceptions.main import FLOpsManagerException
from flops_utils.logging import colorful_logger as logger

flops_blp = flask_openapi3.APIBlueprint(
    "flops",
    __name__,
    url_prefix="/api/flops",
)


@flops_blp.post("/")
def post_fl_service() -> Tuple[dict, HTTPStatus]:
    try:
        handle_new_flops_project(
            request_data=flask.request.json,
            bearer_token=flask.request.headers.get("Authorization"),
        )
    except FLOpsManagerException as e:
        logger.exception(f"{e.msg}, {e.http_status}")
        notify_ui(msg=e.message, flops_project_id=e.flops_project_id)
        return {"message": e.msg}, e.http_status or HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        err_msg = "Unexpected exception occurred"
        logger.exception(err_msg)
        return {"message": f"{err_msg}:{e}"}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {"message": "New FLOps project started successfully"}, HTTPStatus.OK
