from http import HTTPStatus
from typing import Tuple

import flask
import flask_openapi3
from flops_manager.flops_management import handle_new_mock_data_provider
from flops_manager.utils.exceptions.main import FLOpsManagerException
from flops_utils.logging import colorful_logger as logger

mock_data_provider_blp = flask_openapi3.APIBlueprint(
    "flops",
    __name__,
    url_prefix="/api/flops/mocks",
)


@mock_data_provider_blp.post("/")
def post_mock_data_provider() -> Tuple[dict, HTTPStatus]:
    try:
        handle_new_mock_data_provider(
            request_data=flask.request.json,
            bearer_token=flask.request.headers.get("Authorization"),
        )
    except FLOpsManagerException as e:
        e.log()
        return {"message": e.message}, e.http_status or HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        err_msg = "Unexpected exception occurred"
        logger.exception(err_msg)
        return {"message": f"{err_msg}:{e}"}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {"message": "New Mock-Data-Provider started successfully"}, HTTPStatus.OK
