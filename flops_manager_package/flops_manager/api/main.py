from http import HTTPStatus

import flask_openapi3
import flops_manager.api.blueprints as blps
from flops_manager.utils.env_vars import FLOPS_MANAGER_PORT
from waitress import serve

_info = flask_openapi3.Info(title="FLOps Manager API", version="1.0.0")
app = flask_openapi3.OpenAPI(__name__, info=_info)


@app.route("/", methods=["GET"])
def health():
    return {"message": "ok"}, HTTPStatus.OK


def handle_api():
    for blp in blps.blueprints:
        app.register_api(blp)

    # Note (AFAIK): 'waitress' comes with its own logger.
    # We are already using the flops logger.
    # Thus we have duplicated logger outputs (not just for API things but generally).
    # To avoid this the waitress ones gets muted.
    # If something should be logged that concerns the API it will be logged via the flops logger.
    serve(app, host="0.0.0.0", port=FLOPS_MANAGER_PORT, _quiet=True)
