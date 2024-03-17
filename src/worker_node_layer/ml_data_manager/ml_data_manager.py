import os
from http import HTTPStatus

import flask_openapi3
from blueprints import blueprints
from utils.certificate_generator import CERT_PATH, KEY_PATH, handle_certificate

ML_DATA_MANAGER_PORT = os.environ.get("ML_DATA_MANAGER_PORT")

info = flask_openapi3.Info(title="ML Data Manager API", version="1.0.0")
app = flask_openapi3.OpenAPI(__name__, info=info)


@app.route("/", methods=["GET"])
def health():
    return {"message": "ok"}, HTTPStatus.OK


def main():
    for blp in blueprints:
        app.register_api(blp)
    handle_certificate()

    app.run(
        host="0.0.0.0",
        port=ML_DATA_MANAGER_PORT,
        debug=True,
        ssl_context=(str(CERT_PATH), str(KEY_PATH)),
    )


if __name__ == "__main__":
    main()
