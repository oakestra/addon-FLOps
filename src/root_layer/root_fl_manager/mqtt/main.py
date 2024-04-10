import json
import os

import flops.classes.builder.management as builder_management
import paho.mqtt.client as paho_mqtt
import utils.classes.exceptions as custom_exceptions
from mqtt.utils import Topics, reconnect
from utils.logging import logger

# TODO os.environ.get("ROOT_FL_MQTT_BROKER_URL")
ROOT_FL_MQTT_BROKER_URL = "192.168.178.44"
ROOT_FL_MQTT_BROKER_PORT = os.environ.get("ROOT_FL_MQTT_BROKER_PORT")

_mqtt_client = None


def _on_new_message(client, userdata, message) -> None:
    try:
        decoded_message = message.payload.decode()
        data = json.loads(decoded_message)
        logger.debug(f"Received message: {decoded_message}")
        topic = message.topic
        match topic:
            case Topics.IMAGE_BUILDER_SUCCESS.value:
                builder_management.handle_builder_success(builder_success_msg=data)

            case Topics.IMAGE_BUILDER_FAILED.value:
                builder_management.handle_builder_failed(builder_failed_msg=data)

            case Topics.FL_UI_FAILED.value:
                logger.critical(data)

            case _:
                logger.error(f"Message received for an unsupported topic '{topic}'")

    except custom_exceptions.RootFLManagerException as e:
        logger.fatal(f"{e.msg}")
        e.try_to_notify_ui()
        return
    except Exception as e:
        err_msg = f"Unexpected error occured: {e}"
        logger.fatal(err_msg)
        return


def handle_mqtt() -> None:
    mqtt_client = get_mqtt_client()
    for topic in Topics:
        mqtt_client.subscribe(str(topic))
    mqtt_client.loop_forever()


def _init_mqtt() -> paho_mqtt.Client:
    global _mqtt_client
    _mqtt_client = paho_mqtt.Client(paho_mqtt.CallbackAPIVersion.VERSION1)

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            logger.error("ROOT MQTT: Unexpected MQTT disconnection. Attempting to reconnect.")
            reconnect(client)

    _mqtt_client.on_disconnect = on_disconnect
    _mqtt_client.on_message = _on_new_message

    _mqtt_client.connect(ROOT_FL_MQTT_BROKER_URL, int(ROOT_FL_MQTT_BROKER_PORT))
    return _mqtt_client


def get_mqtt_client():
    if _mqtt_client is None:
        return _init_mqtt()
    else:
        return _mqtt_client
