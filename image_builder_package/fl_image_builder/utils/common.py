import shlex
import subprocess


def run_in_bash(bash_cmd: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(shlex.split(bash_cmd), capture_output=True)
