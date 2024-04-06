import hashlib
import json

from utils.classes.base import FlOpsBaseClass


def generate_ip(flops_id: str, object: FlOpsBaseClass) -> str:
    # Note: These numerical gymnastics are intended to avoid IP collisions.
    unique_int = int(flops_id, 16) % 65536
    hash_offset = hashlib.md5(json.dumps(object.to_dict()).encode("utf-8")).digest()
    int_offset = int.from_bytes(hash_offset, byteorder="big")
    magic_number = (unique_int + int_offset) % (10**6)

    third_octet = int(str(magic_number)[0:3]) % 256
    forth_octet = int(str(magic_number)[4:7]) % 256
    return f"10.30.{third_octet}.{forth_octet}"
