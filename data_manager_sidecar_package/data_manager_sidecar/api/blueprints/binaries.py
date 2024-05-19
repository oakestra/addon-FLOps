import pathlib
from datetime import datetime
from http import HTTPStatus

import flask
import flask_openapi3

CONTENT_TYPE = "application/octet-stream"
DATA_VOLUME = pathlib.Path("/flops_data_manager_sidecar_volume")

binaries_blp = flask_openapi3.APIBlueprint(
    "binaries",
    __name__,
    url_prefix="/api/data/binaries",
)


@binaries_blp.post("/")
def post_binary_data():

    if flask.request.headers.get("Content-Type") != CONTENT_TYPE:
        return {
            "error": f"Bad request, the Header Content-Type should be '{CONTENT_TYPE}'"
        }, HTTPStatus.BAD_REQUEST

    binary_data = flask.request.data

    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")
    with open(f"{DATA_VOLUME / current_time}.bin", "wb") as file:
        file.write(binary_data)

    return {"message": "Data posted successfully"}, HTTPStatus.OK
