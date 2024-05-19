from data_manager.api.main import handle_api
from flops_utils.logging import logger


def main():
    logger.info("FLOps Manager started.")
    handle_api()


if __name__ == "__main__":
    main()
