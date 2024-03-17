import os
import pathlib

from utils.common import run_in_bash

CAROOT_PATH = pathlib.Path(os.environ.get("CAROOT"))

CA_KEY_PATH = CAROOT_PATH / "rootCA-key.pem"
CA_CERT_PATH = CAROOT_PATH / "rootCA.pem"

REGISTRY_KEY_PATH = CAROOT_PATH / "registry-key.pem"
REGISTRY_CERT_PATH = CAROOT_PATH / "registry.pem"


# TODO find a better way of doing this - the optimal solution whould be
# a proper OAK CA but this does not seem to fit into my time budget
# So for not I use the mkcert utility that is not recommended to be used on prod systems
# TODO I generate these cerst here but primarily need them for the root image registy
# - I share them via volumes
# Issue is that at the very first launch of these containers
# - where the volumes are empty but the registry container expect to find these certs
# it will fail - need a nice work around.
def handle_ca_and_certificates() -> None:
    if not CA_KEY_PATH.exists() or not CA_CERT_PATH.exists():
        run_in_bash("mkcert -install")
    if not REGISTRY_KEY_PATH.exists() or not REGISTRY_CERT_PATH.exists():
        run_in_bash(
            " ".join(
                (
                    "mkcert",
                    f"-cert-file {CAROOT_PATH}/registry.pem",
                    f"-key-file {CAROOT_PATH}/registry-key.pem",
                    "192.168.178.44",
                    "localhost",
                )
            )
        )
