from flops_manager.mqtt.main import get_mqtt_client
from flops_utils.logging import colorful_logger as logger
from flops_utils.mqtt_topics import Target


def notify_project_observer(
    msg: str,
    flops_project_id: str = "",
) -> None:
    # NOTE: The communication from the FLOps Manager to the Project Observers
    # does not work via Python sockets.
    # The Manager lacks OAK networking capabilities because it is not deployed as a OAK service.
    # Thus we use MQTT instead.
    if not flops_project_id:
        logger.debug(f"Received message '{msg}' without any flops_project_id")
        return

    logger.debug(
        f"Sending message '{msg}' to the Project Observer with FLOps ID: '{flops_project_id}'"
    )
    get_mqtt_client().publish(
        topic=f"{Target.PROJECT_OBSERVER}/{flops_project_id}",
        payload=msg,
        qos=2,
        retain=True,
    )
