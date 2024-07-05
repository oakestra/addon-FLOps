import time

import paho.mqtt.client as paho_mqtt
from flops_manager.utils.env_vars import FLOPS_MQTT_BROKER_IP, FLOPS_MQTT_BROKER_PORT
from flops_utils.logging import colorful_logger as logger

_mqtt_client = None


class FLOpsMQTTDisconnectedException(Exception):
    # NOTE: This exception is not part of the other FLOps exceptions.
    # The project ones will trigger a mqtt based call to the Project Observer.
    # If the MQTT is no longer working it cannot be reached.
    pass


def _reconnect(client):
    FIRST_RECONNECT_DELAY = 1
    RECONNECT_RATE = 2
    MAX_RECONNECT_COUNT = 12
    MAX_RECONNECT_DELAY = 60
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logger.debug("FLOPS MQTT: Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logger.debug("FLOPS MQTT: Reconnected successfully!")
            return
        except Exception as err:
            logger.error("FLOPS MQTT: %s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    raise FLOpsMQTTDisconnectedException()


def _init_mqtt() -> paho_mqtt.Client:
    global _mqtt_client
    _mqtt_client = paho_mqtt.Client(paho_mqtt.CallbackAPIVersion.VERSION2)  # type: ignore

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            logger.error("FLOPS MQTT: Unexpected MQTT disconnection. Attempting to reconnect.")
            _reconnect(client)

    _mqtt_client.on_disconnect = on_disconnect

    _mqtt_client.connect(
        FLOPS_MQTT_BROKER_IP,
        int(FLOPS_MQTT_BROKER_PORT),
    )
    return _mqtt_client


def get_mqtt_client():
    if _mqtt_client is None:
        return _init_mqtt()
    else:
        return _mqtt_client
