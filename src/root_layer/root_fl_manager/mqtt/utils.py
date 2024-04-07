import time

import utils.classes.exceptions as custom_exceptions
from utils.classes.auxiliary import CustomEnum
from utils.logging import logger


class Topics(CustomEnum):
    IMAGE_BUILDER_SUCCESS = "root_fl_manager/image_builder/success"
    IMAGE_BUILDER_FAILED = "root_fl_manager/image_builder/failed"
    FL_UI_FAILED = "root_fl_manager/fl_ui/failed"


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
    raise custom_exceptions.MQTTException("ROOT MQTT: Reconnect failed after %s attempts.")
