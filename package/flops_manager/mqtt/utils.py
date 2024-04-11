import time

import flops_manager.utils.exceptions as flops_exceptions
from flops_manager.utils.logging import logger
from flops_manager.utils.types import CustomEnum


class Topics(CustomEnum):
    IMAGE_BUILDER_SUCCESS = "flops_manager/image_builder/success"
    IMAGE_BUILDER_FAILED = "flops_manager/image_builder/failed"
    FLOPS_UI_FAILED = "flops_manager/flops_ui/failed"


def reconnect(client):
    FIRST_RECONNECT_DELAY = 1
    RECONNECT_RATE = 2
    MAX_RECONNECT_COUNT = 12
    MAX_RECONNECT_DELAY = 60
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logger.debug("ROOT MQTT: Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logger.debug("ROOT MQTT: Reconnected successfully!")
            return
        except Exception as err:
            logger.error("ROOT MQTT: %s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    raise flops_exceptions.MQTTException("ROOT MQTT: Reconnect failed after %s attempts.")
