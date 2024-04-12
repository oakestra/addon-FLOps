# Note: The reason for splitting the listener and sender is to avoid cyclic dependency issues.

import json

from flops_manager.classes.oakestratables.deployables.internal.builder.termination import (
    handle_builder_failed,
    handle_builder_success,
)
from flops_manager.mqtt.constants import Topics
from flops_manager.mqtt.main import get_mqtt_client
from flops_manager.utils.exceptions.main import FLOpsManagerException
from flops_manager.utils.logging import logger


def _on_new_message(client, userdata, message) -> None:
    try:
        decoded_message = message.payload.decode()
        data = json.loads(decoded_message)
        logger.debug(f"Received message: {decoded_message}")
        topic = message.topic
        match topic:
            case Topics.IMAGE_BUILDER_SUCCESS.value:
                handle_builder_success(builder_success_msg=data)

            case Topics.IMAGE_BUILDER_FAILED.value:
                handle_builder_failed(builder_failed_msg=data)

            case Topics.FLOPS_UI_FAILED.value:
                logger.critical(data)

            case _:
                logger.error(f"Message received for an unsupported topic '{topic}'")

    except FLOpsManagerException as e:
        logger.fatal(f"{e.msg}")
        e.try_to_notify_ui()
        return
    except Exception as e:
        err_msg = f"Unexpected error occured: {e}"
        logger.fatal(err_msg)
        return


def init_mqtt_listener() -> None:
    mqtt_client = get_mqtt_client()
    mqtt_client.on_message = _on_new_message
    for topic in Topics:
        mqtt_client.subscribe(str(topic))
    mqtt_client.loop_forever()
