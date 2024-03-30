import mqtt.main
from utils.identifier import FlOpsIdentifier
from utils.logging import logger


def notify_ui(
    msg: str,
    flops_identifier: FlOpsIdentifier,
) -> None:
    # NOTE: RFLM -> FLUI does not work via python sockets !
    # Because RFLM is not deployed as a OAK service -> it lacks OAK networking capabilities
    # One way I see to realize RFLM <-> FLUI communication is via RFLM's MQTT !!
    logger.debug(f"Sending message '{msg}' to FLGUI {flops_identifier.fl_ui_ip}")
    mqtt.main.get_mqtt_client().publish(
        topic=f"flui/{flops_identifier.flops_id}",
        payload=msg,
        # TODO - test and try out other QOS
        # - QOS 2 seems to be the way to go but initial tests failed
        qos=1,
        retain=False,
    )
