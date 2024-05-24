import io
import os
import pathlib
import zipfile
from datetime import datetime
from http import HTTPStatus

import flask
import flask_openapi3
import netaddr
from flask import send_file

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


@binaries_blp.get("/")
def get_binary_data():
    client_ip = flask.request.remote_addr

    from flops_utils.logging import logger

    logger.info(f"client_ip = {client_ip}")

    # We only allow getting the ML data for the co-located FLOps services/containers.
    if not netaddr.IPAddress(client_ip).is_ipv4_private_use():
        return {"error": "Access denied"}, 403

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for file_name in DATA_VOLUME.glob("*.bin"):
            zf.write(file_name, arcname=os.path.basename(file_name))

    # Reset the buffer pointer to the beginning of the ZIP file
    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name="all_binaries.zip",
        mimetype="application/zip",
    )
