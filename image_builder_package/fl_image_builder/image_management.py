import os
import pathlib
import shlex
import subprocess

from context.main import get_context
from flops_utils.logging import colorful_logger as logger
from notification_management import notify_about_failed_build_and_terminate, notify_ui
from utils.common import (
    FL_AGGREGATOR_IMAGE_PATH,
    FL_BASE_IMAGE_PATH,
    FL_LEARNER_IMAGE_PATH,
)
from utils.devel_base_images import DEVEL_BASE_IMAGES_MAPPING
from utils.timeframes import (
    BASE_IMAGE_BUILD_TIMEFRAME,
    BUILD_ALL_IMAGES_TIMEFRAME,
    IMAGE_PUSH_TIMEFRAME,
)

FL_BASE_IMAGE_NAME = "fl_base"


def prepare_new_image_names() -> None:
    full_registry_url = get_context().image_registry_url
    cloned_repo = get_context().cloned_repo

    image_registry_url = full_registry_url.removeprefix("http://").removeprefix(
        "https://"
    )
    latest_commit_hash = cloned_repo.head.commit.hexsha

    repo_url = cloned_repo.remotes.origin.url
    user_repo_name = repo_url.split("github.com/")[1].split(".git")[0]
    # Note: (docker) image registry URLs do now allow uppercases.
    username = user_repo_name.split("/")[0].lower()
    repo_name = user_repo_name.split("/")[1]

    get_context().set_new_image_name_prefix(
        f"{image_registry_url}/{username}/{repo_name}"
    )
    get_context().set_new_image_tag(latest_commit_hash)


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


def _build_base_image() -> None:
    get_context().timer.start_new_time_frame(BASE_IMAGE_BUILD_TIMEFRAME)
    if get_context().use_devel_base_images:
        build_image(
            build_directory=FL_BASE_IMAGE_PATH,
            is_flops_base_image=True,
            base_image_to_use=DEVEL_BASE_IMAGES_MAPPING[get_context().repo_url],
        )
    else:
        build_image(build_directory=FL_BASE_IMAGE_PATH, is_flops_base_image=True)

    get_context().timer.end_time_frame(BASE_IMAGE_BUILD_TIMEFRAME)


def build_images() -> None:
    get_context().timer.start_new_time_frame(BUILD_ALL_IMAGES_TIMEFRAME)

    _build_base_image()

    build_image(
        build_directory=FL_LEARNER_IMAGE_PATH,
        image_name_with_tag=get_context().get_learner_image_name(),
        base_image_to_use=FL_BASE_IMAGE_NAME,
    )

    build_image(
        build_directory=FL_AGGREGATOR_IMAGE_PATH,
        image_name_with_tag=get_context().get_aggregator_image_name(),
        base_image_to_use=FL_BASE_IMAGE_NAME,
    )
    get_context().timer.end_time_frame(BUILD_ALL_IMAGES_TIMEFRAME)


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


def push_images() -> None:
    get_context().timer.start_new_time_frame(IMAGE_PUSH_TIMEFRAME)
    push_image(get_context().get_learner_image_name())
    push_image(get_context().get_aggregator_image_name())
    get_context().timer.end_time_frame(IMAGE_PUSH_TIMEFRAME)
