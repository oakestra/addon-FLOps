import os
import shlex
import subprocess

# TODO
FLOPS_MANAGER_IP = "192.168.178.44"
FLOPS_MANAGER_PORT = os.environ.get("FLOPS_MANAGER_PORT")

FLOPS_USER_ACCOUNT = "Infrastructure_Provider"

FLOPS_SERVICE_CMD_PREFIX = "poetry run python main.py"


def run_in_bash(bash_cmd: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(shlex.split(bash_cmd), capture_output=True, check=True)
