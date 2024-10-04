import json
import socket
import sys

import paho.mqtt.client as paho_mqtt

from flops_utils.logging import logger
from flops_utils.mqtt_topics import SupportedTopic


def notify_project_observer(project_observer_ip: str, msg: str) -> None:
    logger.debug(f"Sending message to the project observer: {msg}")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((project_observer_ip, 2727))
    client_socket.send(msg.encode())
    client_socket.close()
    logger.debug(f"Send message to the project observer: {msg}")
    sys.stdout.flush()


def notify_flops_manager(
    flops_project_id: str,
    mqtt_ip: str,
    topic: SupportedTopic,
    msg_payload: dict = {},
    error_msg: str = "",
    mqtt_port: int = 9027,
) -> None:

    payload = msg_payload.copy()
    payload.update(
        {
            "flops_project_id": flops_project_id,
            **({"error_msg": error_msg} if error_msg else {}),
        }
    )
    mqtt_client = paho_mqtt.Client(paho_mqtt.CallbackAPIVersion.VERSION1)  # type: ignore
    mqtt_client.connect(mqtt_ip, mqtt_port)
    mqtt_client.publish(
        topic=topic.value,
        payload=json.dumps(payload),
        # Note: qos=2 should be used, however qos=2 does not work for some reason.
        # The client seems to properly send the message and terminate.
        # But the server does not receive the message..
        qos=1,
        retain=False,
    )
    logger.debug(f"Send message to FLOps Manager: {str(payload)}")
