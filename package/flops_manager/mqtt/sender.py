from flops_manager.mqtt.main import get_mqtt_client
from flops_manager.utils.logging import logger


def notify_ui(
    msg: str,
    flops_project_id: str,
) -> None:
    # NOTE: RFLM -> FLUI does not work via python sockets !
    # Because RFLM is not deployed as a OAK service -> it lacks OAK networking capabilities
    # One way I see to realize RFLM <-> FLUI communication is via RFLM's MQTT !!
    logger.debug(f"Sending message '{msg}' to FL UI for FLOps: '{flops_project_id}'")
    get_mqtt_client().publish(
        topic=f"flopsui/{flops_project_id}",
        payload=msg,
        qos=2,
        retain=True,
    )
