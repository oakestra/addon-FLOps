from flops_utils.logging import logger
from ml_data_server.flight_server import handle_server


def main():
    logger.info("FLOps Manager started.")
    handle_server()


if __name__ == "__main__":
    main()
