import hashlib

from pydantic import BaseModel


def get_shortened_unique_id(id: str) -> str:
    return hashlib.md5(id.encode()).digest()[:6].hex()


def generate_ip(unique_id: str, object: BaseModel) -> str:
    # NOTE: These numerical gymnastics are intended to avoid IP collisions.
    # TODO/Future work: this logic needs to be more bullet proof.
    # I.e. we need to ask the OAK components for available IPs instead of conjuring one ourselves.

    unique_int = int(unique_id, 16) % 65536

    type_based_hash_offset = hash(type(object))
    magic_number = (unique_int + type_based_hash_offset) % (10**6)

    third_octet = int(str(magic_number)[0:3]) % 256
    forth_octet = int(str(magic_number)[4:7]) % 256

    return f"10.30.{third_octet}.{forth_octet}"
