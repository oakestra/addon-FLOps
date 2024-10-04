import shlex
import subprocess


def run_in_shell(
    shell_cmd: str,
    capture_output=True,
    check=True,
    text=False,
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        shlex.split(shell_cmd), capture_output=capture_output, check=check, text=text
    )
