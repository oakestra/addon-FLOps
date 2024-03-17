import json
import os
import time

import paho.mqtt.client as paho_mqtt
from api.common import GITHUB_PREFIX
from fl_services.main import handle_new_fl_service, handle_builder_success, handle_builder_failed
from utils.logging import logger
from mqtt.enums import Topics


ROOT_MQTT_BROKER_URL = os.environ.get("ROOT_MQTT_BROKER_URL")
ROOT_MQTT_BROKER_PORT = os.environ.get("ROOT_MQTT_BROKER_PORT")


def _reconnect(client) -> None:
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
            logger.info("ROOT MQTT: Reconnected successfully!")
            return
        except Exception as err:
            logger.error("ROOT MQTT: %s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logger.fatal("ROOT MQTT: Reconnect failed after %s attempts. Exiting...", reconnect_count)


def _on_new_message(client, userdata, message) -> None:
    decoded_message = message.payload.decode()
    data = json.loads(decoded_message)
    logger.debug(f"Received message: {decoded_message}")
    topic = message.topic
    match topic:
        case Topics.NEW_SERVICES.value:
            if data["virtualization"] == "ml-repo" and data["code"].startswith(GITHUB_PREFIX):
                handle_new_fl_service(data)
                
        case Topics.IMAGE_BUILDER_SUCCESS.value:
            handle_builder_success(data)
            
        case Topics.IMAGE_BUILDER_FAILED.value:
            handle_builder_failed(data)
            
        case _:
            logger.error(f"Message received for an unsupported topic '{topic}'")


def handle_mqtt() -> None:
    mqtt_client = paho_mqtt.Client(paho_mqtt.CallbackAPIVersion.VERSION1)

    def _on_disconnect(client, userdata, rc) -> None:
        if rc != 0:
            logger.error("ROOT MQTT: Unexpected MQTT disconnection. Attempting to reconnect.")
            _reconnect(client)

    mqtt_client.on_disconnect = _on_disconnect
    mqtt_client.on_message = _on_new_message
    mqtt_client.connect(ROOT_MQTT_BROKER_URL, int(ROOT_MQTT_BROKER_PORT))
    for topic in Topics:
        mqtt_client.subscribe(str(topic))
    mqtt_client.loop_forever()
