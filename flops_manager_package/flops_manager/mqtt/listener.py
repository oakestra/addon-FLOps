# Note: The reason for splitting the listener and sender is to avoid cyclic dependency issues.

import json

from flops_manager.classes.deployables.project_services.aggregator.termination import (
    handle_aggregator_failed,
    handle_aggregator_success,
)
from flops_manager.classes.deployables.project_services.builder.termination import (
    handle_builder_failed,
    handle_builder_success,
)
from flops_manager.mqtt.constants import Topics
from flops_manager.mqtt.main import get_mqtt_client
from flops_manager.mqtt.sender import notify_project_observer
from flops_manager.utils.exceptions.main import FLOpsManagerException
from flops_utils.logging import colorful_logger as logger


def _on_new_message(client, userdata, message) -> None:
    try:
        decoded_message = message.payload.decode()
        data = json.loads(decoded_message)
        topic = message.topic
        logger.debug(f"Received message: '{decoded_message}' for topic '{topic}'")
        match topic:

            case Topics.PROJECT_OBSERVER_FAILED.value:
                logger.critical(data)

            case Topics.IMAGE_BUILDER_SUCCESS.value:
                handle_builder_success(builder_success_msg=data)
            case Topics.IMAGE_BUILDER_FAILED.value:
                handle_builder_failed(builder_failed_msg=data)

            case Topics.AGGREGATOR_SUCCESS.value:
                handle_aggregator_success(aggregator_success_msg=data)
            case Topics.AGGREGATOR_FAILED.value:
                handle_aggregator_failed(aggregator_failed_msg=data)

            case _:
                logger.error(f"Message received for an unsupported topic '{topic}'")

    except FLOpsManagerException as e:
        logger.exception(f"{e.message}")
        notify_project_observer(flops_project_id=e.flops_project_id, msg=e.message)
        return
    except Exception:
        logger.exception("Unexpected exception occurred")
        return


def init_mqtt_listener() -> None:
    mqtt_client = get_mqtt_client()
    mqtt_client.on_message = _on_new_message
    for topic in Topics:
        mqtt_client.subscribe(str(topic))
    mqtt_client.loop_forever()
