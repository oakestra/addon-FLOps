import json
import sys
import time

import paho.mqtt.client as paho_mqtt
from flops_utils.logging import logger
from project_observer.ui_context import get_ui_context

_mqtt_client = None


def _on_new_message(client, userdata, message) -> None:
    decoded_message = message.payload.decode()
    logger.debug(decoded_message)


def _reconnect(client):

    FIRST_RECONNECT_DELAY = 1
    RECONNECT_RATE = 2
    MAX_RECONNECT_COUNT = 12
    MAX_RECONNECT_DELAY = 60
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logger.debug("FLOps MQTT: Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logger.debug("FLOps MQTT: Reconnected successfully!")
            return
        except Exception as err:
            logger.error("FLOps MQTT: %s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logger.fatal("FLOps MQTT: Reconnect failed after %s attempts. Exiting...", reconnect_count)


def _init_mqtt() -> paho_mqtt.Client:

    global _mqtt_client
    _mqtt_client = paho_mqtt.Client(paho_mqtt.CallbackAPIVersion.VERSION1)

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            logger.error("FLOps MQTT: Unexpected MQTT disconnection. Attempting to reconnect.")
            _reconnect(client)

    _mqtt_client.on_disconnect = on_disconnect
    _mqtt_client.on_message = _on_new_message

    _mqtt_client.connect(get_ui_context().mqtt_ip, int(get_ui_context().mqtt_port))
    return _mqtt_client


def get_mqtt_client():
    if _mqtt_client is None:
        return _init_mqtt()
    else:
        return _mqtt_client


def handle_mqtt() -> None:
    mqtt_client = get_mqtt_client()
    mqtt_client.subscribe(f"flopsui/{get_ui_context().flops_id}")
    mqtt_client.loop_forever()


def notify_flops_manager(error_msg: str = None) -> None:
    ui_context = get_ui_context()
    payload = json.dumps(
        {
            "flops_id": ui_context.flops_id,
            **({"error_msg": error_msg} if error_msg is not None else {}),
        }
    )
    get_mqtt_client().publish(
        topic="flops_manager/project_observer/failed",
        payload=payload,
        qos=2,
        retain=False,
    )
    logger.debug(f"Send message to FLOps Manager: {str(payload)}")
    sys.exit(1)
