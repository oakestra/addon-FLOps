from http import HTTPStatus
from typing import Tuple

import flask
import flask_openapi3
from flops_manager.manage_flops import handle_new_flops_project
from flops_manager.mqtt.sender import notify_ui
from flops_manager.utils.exceptions.main import FLOpsManagerException
from flops_manager.utils.logging import logger

flops_blp = flask_openapi3.APIBlueprint(
    "flops",
    __name__,
    url_prefix="/api/flops",
)


@flops_blp.post("/")
def post_fl_service() -> Tuple[dict, HTTPStatus]:
    # TODO add sla-schema checking, etc. similar to main repo
    # Note: Current Assumption: A new FL app needs to be created.
    # If the use cases come up that a FL service should be appended to an existing App
    # that can be easily realized.
    try:
        bearer_token = flask.request.headers.get("Authorization")
        handle_new_flops_project(
            new_flops_project_sla=flask.request.json,
            bearer_token=bearer_token,
        )
    except FLOpsManagerException as e:
        logger.fatal(f"{e.msg}, {e.http_status}")
        notify_ui(msg=e.message, flops_project_id=e.flops_project_id)
        return {"message": e.msg}, e.http_status or HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        err_msg = f"Unexpected error occured: {e}"
        logger.fatal(err_msg)
        return {"message": err_msg}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {"message": "New FLOps project started successfully"}, HTTPStatus.OK
