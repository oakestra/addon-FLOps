# Note: The reason for splitting the listener and sender is to avoid cyclic dependency issues.

import json

from flops_manager.classes.services.project.aggregator.termination import (
    handle_aggregator_failed,
    handle_aggregator_success,
)
from flops_manager.classes.services.project.builders.fl_actors_builder import FLActorsImageBuilder
from flops_manager.classes.services.project.builders.trained_model_builder import (
    TrainedModelImageBuilder,
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

            case Topics.FL_ACTORS_IMAGE_BUILDER_SUCCESS.value:
                FLActorsImageBuilder.handle_builder_success(builder_success_msg=data)
            case Topics.FL_ACTORS_IMAGE_BUILDER_FAILED.value:
                FLActorsImageBuilder.handle_builder_failed(builder_failed_msg=data)
            case Topics.TRAINED_MODEL_IMAGE_BUILDER_SUCCESS.value:
                TrainedModelImageBuilder.handle_builder_success(builder_success_msg=data)
            case Topics.TRAINED_MODEL_IMAGE_BUILDER_FAILED.value:
                TrainedModelImageBuilder.handle_builder_failed(builder_failed_msg=data)

            case Topics.AGGREGATOR_SUCCESS.value:
                handle_aggregator_success(aggregator_success_msg=data)
            case Topics.AGGREGATOR_FAILED.value:
                handle_aggregator_failed(aggregator_failed_msg=data)

            case _:
                logger.error(f"Message received for an unsupported topic '{topic}'")

    except FLOpsManagerException as e:
        e.log()
        if e.flops_project_id:
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
