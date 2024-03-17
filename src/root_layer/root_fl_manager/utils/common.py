import os
import shlex
import subprocess

# TODO
ROOT_FL_MANAGER_IP = "192.168.178.44"
ROOT_FL_MANAGER_PORT = os.environ.get("ROOT_FL_MANAGER_PORT")

FLOPS_USER_ACCOUNT = "Infrastructure_Provider"


def run_in_bash(bash_cmd: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(shlex.split(bash_cmd), capture_output=True, check=True)
