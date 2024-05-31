import os
import pathlib
import shlex
import subprocess

from context.main import get_context
from flops_utils.logging import colorful_logger as logger
from notification_management import notify_about_failed_build_and_terminate, notify_ui


def build_image(
    build_directory: str,
    image_name_with_tag: str = None,
    base_image_to_use: str = None,
    is_flops_base_image: bool = False,
) -> None:
    image_name_with_tag = image_name_with_tag or build_directory
    cwd = pathlib.Path.cwd()
    # Important: Be very careful how and where you run buildah.
    # If you run buildah incorrectly it can easily kill your host system.
    # E.g. Mismatch between current directory and target Dockerfile to build.
    os.chdir(build_directory)
    build_start_msg = f"Start building {image_name_with_tag} image"
    if is_flops_base_image:
        build_start_msg += " (This can take a while)"
        notify_ui(f"ML repo successfully cloned & verified.\n{build_start_msg}")
    logger.info(build_start_msg)
    try:
        # TODO read further about buildah options/flags - might improve the build further.
        build_cmd = f"buildah build --isolation=chroot -t {image_name_with_tag}"
        if is_flops_base_image:
            model_flavor = get_context().ml_model_flavor.value
            build_cmd += f" --build-arg ML_MODEL_FLAVOR={model_flavor}"
            if get_context().use_devel_base_images:
                build_cmd += " -f devel.Dockerfile"
        if base_image_to_use:
            build_cmd += f" --build-arg BASE_IMAGE={base_image_to_use}"
            if get_context().use_devel_base_images:
                build_cmd += f" --build-arg USE_DEVEL_BASE_IMAGES={True}"
        result = subprocess.run(
            shlex.split(build_cmd),
            check=False,
            text=True,
        )
        if result.returncode != 0:
            notify_about_failed_build_and_terminate(
                f"Image build for '{image_name_with_tag}' completed with rc != 0; '{result.stderr}'"
            )
    except Exception as e:
        notify_about_failed_build_and_terminate(
            f"Image build process for '{image_name_with_tag}' failed; '{e}'"
        )
    build_fin_msg = f"Successfully finished building new '{image_name_with_tag}' image"
    logger.info(build_fin_msg)
    if is_flops_base_image:
        notify_ui(build_fin_msg)
    os.chdir(cwd)


def push_image(image_name_with_tag: str) -> None:
    logger.info(f"Start pushing image '{image_name_with_tag}'")
    try:
        subprocess.check_call(
            shlex.split(f"buildah push --tls-verify=false  {image_name_with_tag}")
        )
    except Exception as e:
        notify_about_failed_build_and_terminate(
            f"Failed to push '{image_name_with_tag}' to image registry; '{e}'"
        )
    push_fin_msg = f"Successfully pushed new '{image_name_with_tag}' image"
    logger.info(push_fin_msg)
    notify_ui(push_fin_msg)
