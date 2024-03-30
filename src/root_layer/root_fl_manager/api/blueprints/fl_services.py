from http import HTTPStatus

import flask
import flask_openapi3
from fl_services.main import handle_new_fl_service

flops_blp = flask_openapi3.APIBlueprint(
    "flops",
    __name__,
    url_prefix="/api/flops",
)


@flops_blp.post("/")
def post_fl_service():
    # TODO add sla-schema checking, etc. similar to main repo
    # Note: Current Assumption: A new FL app needs to be created.
    # If the use cases come up that a FL service should be appended to an existing App
    # that can be easily realized.
    data = flask.request.json
    bearer_token = flask.request.headers.get("Authorization")
    verbose = data["verbose"]
    handle_new_fl_service(data, bearer_token, verbose)
    return {"message": "New FLOps processes started"}, HTTPStatus.OK
