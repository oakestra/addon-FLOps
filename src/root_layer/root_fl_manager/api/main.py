from http import HTTPStatus

import api.blueprints as blps
import flask_openapi3
from api.consts import ROOT_FL_MANAGER_PORT

_info = flask_openapi3.Info(title="Root FL Manager API", version="1.0.0")
app = flask_openapi3.OpenAPI(__name__, info=_info)


@app.route("/", methods=["GET"])
def health():
    return {"message": "ok"}, HTTPStatus.OK


def handle_api():
    for blp in blps.blueprints:
        app.register_api(blp)
    app.run(
        host="0.0.0.0",
        port=ROOT_FL_MANAGER_PORT,
        debug=False,
    )
