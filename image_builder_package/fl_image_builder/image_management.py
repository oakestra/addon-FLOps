from __future__ import annotations

import os
import pathlib
from typing import TYPE_CHECKING

from flops_utils.logging import colorful_logger as logger
from flops_utils.shell import run_in_shell
from notification_management import notify_observer

if TYPE_CHECKING:
    from context.main import Context


def build_image(
    context: Context,
    build_directory: str,
    image_name_with_tag: str = "",
    base_image_to_use: str = "",
    should_notify_observer: bool = False,
    build_cmd_addition: str = "",
) -> None:
    image_name_with_tag = (
        image_name_with_tag or build_directory or context.get_image_name()
    )
    cwd = pathlib.Path.cwd()
    # Important: Be very careful how and where you run buildah.
    # If you run buildah incorrectly it can easily kill your host system.
    # E.g. Mismatch between current directory and target Dockerfile to build.
    os.chdir(build_directory)
    build_start_msg = f"Start building {image_name_with_tag} image"
    build_start_msg += " (This can take a while)"
    if should_notify_observer:
        notify_observer(context=context, msg=build_start_msg)
    logger.info(build_start_msg)
    platforms = " ".join(
        [f"--platform {platform.value}" for platform in context.supported_platforms]
    )
    # TODO read further about buildah options/flags - might improve the build further.
    build_cmd = " ".join(
        (
            "buildah build",
            platforms,
            "--isolation=chroot",
            "--tls-verify=false",
            f"--manifest {image_name_with_tag}-manifest",
            f"-t {image_name_with_tag}",
        )
    )
    if base_image_to_use:
        build_cmd += f" --build-arg BASE_IMAGE={base_image_to_use}"
    if build_cmd_addition:
        build_cmd += build_cmd_addition
    try:
        result = run_in_shell(shell_cmd=build_cmd, check=False, text=True)
        if result.returncode != 0:
            context.notify_about_failed_build_and_terminate(
                f"Image build for '{image_name_with_tag}' completed with rc != 0; '{result.stderr}'"
            )
    except Exception as e:
        context.notify_about_failed_build_and_terminate(
            f"Image build process for '{image_name_with_tag}' failed; '{e}'"
        )
    build_fin_msg = f"Successfully finished building new '{image_name_with_tag}' image"
    logger.info(build_fin_msg)
    if should_notify_observer:
        notify_observer(context=context, msg=build_fin_msg)
    os.chdir(cwd)


def push_image(context: Context, image_name_with_tag: str = "") -> None:
    image_name_with_tag = image_name_with_tag or context.get_image_name()
    logger.info(f"Start pushing image '{image_name_with_tag}'")
    cmd = " ".join(
        (
            "buildah",
            "manifest push",
            "--tls-verify=false",
            "--all",
            f"{image_name_with_tag}-manifest",
            # https://github.com/containers/image/blob/main/docs/containers-transports.5.md#dockerdocker-reference
            f"docker://{image_name_with_tag}",
        )
    )

    try:
        run_in_shell(cmd)
    except Exception as e:
        context.notify_about_failed_build_and_terminate(
            f"Failed to push '{image_name_with_tag}' to image registry; '{e}'"
        )
    push_fin_msg = f"Successfully pushed new '{image_name_with_tag}' image"
    logger.info(push_fin_msg)
    notify_observer(context=context, msg=push_fin_msg)
