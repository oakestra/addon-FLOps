from http import HTTPStatus
from typing import Tuple

import flask
import flask_openapi3
from flops_manager.flops_management.flops_projects import handle_new_flops_project
from flops_manager.mqtt.sender import notify_project_observer
from flops_manager.utils.exceptions.main import FLOpsManagerException
from flops_utils.logging import colorful_logger as logger

projects_blp = flask_openapi3.APIBlueprint(
    "projects",
    __name__,
    url_prefix="/api/flops/projects",
)


@projects_blp.post("/")
def post_project() -> Tuple[dict, HTTPStatus]:
    try:
        handle_new_flops_project(
            request_data=flask.request.json,
            bearer_token=flask.request.headers.get("Authorization"),
        )
    except FLOpsManagerException as e:
        e.log()
        if e.flops_project_id:
            notify_project_observer(msg=e.message, flops_project_id=e.flops_project_id)
        return {"message": e.message}, e.http_status or HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        err_msg = "Unexpected exception occurred"
        logger.exception(err_msg)
        return {"message": f"{err_msg}:{e}"}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {"message": "New FLOps project started successfully"}, HTTPStatus.OK
