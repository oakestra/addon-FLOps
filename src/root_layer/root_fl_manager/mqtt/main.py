import json
import os
import time

import image_builder_management.main as image_builder
import paho.mqtt.client as paho_mqtt
import utils.exceptions
from mqtt.enums import Topics
from utils.logging import logger

# TODO os.environ.get("ROOT_FL_MQTT_BROKER_URL")
ROOT_FL_MQTT_BROKER_URL = "192.168.178.44"
ROOT_FL_MQTT_BROKER_PORT = os.environ.get("ROOT_FL_MQTT_BROKER_PORT")

_mqtt_client = None


def _on_new_message(client, userdata, message) -> None:
    decoded_message = message.payload.decode()
    data = json.loads(decoded_message)
    logger.debug(f"Received message: {decoded_message}")
    topic = message.topic
    match topic:
        case Topics.IMAGE_BUILDER_SUCCESS.value:
            image_builder.handle_builder_success(data)

        case Topics.IMAGE_BUILDER_FAILED.value:
            image_builder.handle_builder_failed(data)

        case Topics.FL_UI_FAILED.value:
            logger.critical(data)

        case _:
            logger.error(f"Message received for an unsupported topic '{topic}'")


def handle_mqtt() -> None:
    mqtt_client = get_mqtt_client()
    for topic in Topics:
        mqtt_client.subscribe(str(topic))
    mqtt_client.loop_forever()


def _reconnect(client):

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
    raise utils.exceptions.MQTTException("ROOT MQTT: Reconnect failed after %s attempts.")


def _init_mqtt() -> paho_mqtt.Client:
    global _mqtt_client
    _mqtt_client = paho_mqtt.Client(paho_mqtt.CallbackAPIVersion.VERSION1)

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            logger.error("ROOT MQTT: Unexpected MQTT disconnection. Attempting to reconnect.")
            _reconnect(client)

    _mqtt_client.on_disconnect = on_disconnect
    _mqtt_client.on_message = _on_new_message

    _mqtt_client.connect(ROOT_FL_MQTT_BROKER_URL, int(ROOT_FL_MQTT_BROKER_PORT))
    return _mqtt_client


def get_mqtt_client():
    if _mqtt_client is None:
        return _init_mqtt()
    else:
        return _mqtt_client
