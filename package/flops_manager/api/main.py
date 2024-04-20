from http import HTTPStatus

import flask_openapi3
import flops_manager.api.blueprints as blps
from flops_manager.api.utils.consts import FLOPS_MANAGER_PORT
from waitress import serve

_info = flask_openapi3.Info(title="FLOps Manager API", version="1.0.0")
app = flask_openapi3.OpenAPI(__name__, info=_info)


@app.route("/", methods=["GET"])
def health():
    return {"message": "ok"}, HTTPStatus.OK


def handle_api():
    for blp in blps.blueprints:
        app.register_api(blp)

    serve(app, host="0.0.0.0", port=FLOPS_MANAGER_PORT)
