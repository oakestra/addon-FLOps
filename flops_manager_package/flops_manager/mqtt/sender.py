from flops_manager.mqtt.main import get_mqtt_client
from flops_utils.logging import colorful_logger as logger


def notify_project_observer(
    msg: str,
    flops_project_id: str = None,
) -> None:
    # NOTE: RFLM -> FLUI does not work via python sockets !
    # Because RFLM is not deployed as a OAK service -> it lacks OAK networking capabilities
    # One way I see to realize RFLM <-> FLUI communication is via RFLM's MQTT !!
    if not flops_project_id:
        logger.debug(f"Received message '{msg}' without any flops_project_id")
        return

    logger.debug(f"Sending message '{msg}' to FLOps UI for FLOps: '{flops_project_id}'")
    get_mqtt_client().publish(
        topic=f"flopsui/{flops_project_id}",
        payload=msg,
        qos=2,
        retain=True,
    )
