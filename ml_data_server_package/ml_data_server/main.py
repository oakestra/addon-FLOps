from flops_utils.logging import logger
from ml_data_server.flight_server.main import handle_server


def main():
    logger.info("ML-Data-Server started.")
    handle_server()


if __name__ == "__main__":
    main()
