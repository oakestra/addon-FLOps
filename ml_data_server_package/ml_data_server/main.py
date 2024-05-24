from data_manager_sidecar.api.main import handle_api
from data_manager_sidecar.server.main import handle_server
from flops_utils.logging import logger


def main():
    logger.info("FLOps Manager started.")
    # handle_api()
    handle_server()


if __name__ == "__main__":
    main()
