import hashlib

from flops_manager.flops.classes.abstract.base import FlOpsBaseClass
from flops_manager.mqtt.main import get_mqtt_client
from flops_manager.utils.logging import logger


def generate_ip(flops_id: str, object: FlOpsBaseClass) -> str:
    # Note: These numerical gymnastics are intended to avoid IP collisions.
    unique_int = int(flops_id, 16) % 65536
    hash_offset = hashlib.md5(object.model_dump_json().encode("utf-8")).digest()
    int_offset = int.from_bytes(hash_offset, byteorder="big")
    magic_number = (unique_int + int_offset) % (10**6)

    third_octet = int(str(magic_number)[0:3]) % 256
    forth_octet = int(str(magic_number)[4:7]) % 256
    return f"10.30.{third_octet}.{forth_octet}"


def notify_ui(
    msg: str,
    flops_project_id: str,
) -> None:
    # NOTE: RFLM -> FLUI does not work via python sockets !
    # Because RFLM is not deployed as a OAK service -> it lacks OAK networking capabilities
    # One way I see to realize RFLM <-> FLUI communication is via RFLM's MQTT !!
    logger.debug(f"Sending message '{msg}' to FL UI for FLOps: '{flops_project_id}'")
    get_mqtt_client().publish(
        topic=f"flui/{flops_project_id}",
        payload=msg,
        qos=2,
        retain=True,
    )
