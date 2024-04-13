import shlex
import subprocess

from flops_manager.classes.base import FlOpsBaseClass


def run_in_bash(bash_cmd: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(shlex.split(bash_cmd), capture_output=True, check=True)


def generate_ip(flops_id: str, object: FlOpsBaseClass) -> str:
    # Note: These numerical gymnastics are intended to avoid IP collisions.
    unique_int = int(flops_id, 16) % 65536

    type_based_hash_offset = hash(type(object))
    magic_number = (unique_int + type_based_hash_offset) % (10**6)

    third_octet = int(str(magic_number)[0:3]) % 256
    forth_octet = int(str(magic_number)[4:7]) % 256

    return f"10.30.{third_octet}.{forth_octet}"
