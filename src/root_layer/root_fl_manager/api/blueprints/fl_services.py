from http import HTTPStatus

import flask
import flask_openapi3
from flops.main import handle_new_fl_service
from utils.exceptions import RootFLManagerException
from utils.logging import logger
from utils.types import ExternalApiResponse

flops_blp = flask_openapi3.APIBlueprint(
    "flops",
    __name__,
    url_prefix="/api/flops",
)


@flops_blp.post("/")
def post_fl_service() -> ExternalApiResponse:
    # TODO add sla-schema checking, etc. similar to main repo
    # Note: Current Assumption: A new FL app needs to be created.
    # If the use cases come up that a FL service should be appended to an existing App
    # that can be easily realized.
    data = flask.request.json
    bearer_token = flask.request.headers.get("Authorization")
    verbose = data["verbose"]
    try:
        handle_new_fl_service(data, bearer_token, verbose)

    except RootFLManagerException as e:
        logger.fatal(f"{e.msg}, {e.http_status}")
        e.try_to_notify_ui()
        return {"message": e.msg}, e.http_status or HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        err_msg = f"Unexpected error occured: {e}"
        logger.fatal(err_msg)
        return {"message": err_msg}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {"message": "New FLOps processes started successfully"}, HTTPStatus.OK
