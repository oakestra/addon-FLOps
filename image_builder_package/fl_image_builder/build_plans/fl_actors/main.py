#!/usr/bin/env python3
from __future__ import annotations

from typing import TYPE_CHECKING

from fl_image_builder.build_plans.fl_actors.images.devel_base_images import (
    DEVEL_BASE_IMAGES_MAPPING,
)
from fl_image_builder.build_plans.fl_actors.repo_management import (
    check_cloned_repo,
    clone_repo,
)
from image_management import build_image, push_image
from utils.common import (
    FL_AGGREGATOR_IMAGE_PATH,
    FL_BASE_IMAGE_PATH,
    FL_LEARNER_IMAGE_PATH,
)
from utils.timeframes import (
    BASE_IMAGE_BUILD_TIMEFRAME,
    BUILD_ALL_IMAGES_TIMEFRAME,
    BUILD_PREPARATION_TIMEFRAME,
    IMAGE_PUSH_TIMEFRAME,
)

if TYPE_CHECKING:
    from context.fl_actors import ContextFLActors

_FL_BASE_IMAGE_NAME = "fl_base"


def _prepare_new_image_names(context: ContextFLActors) -> None:
    cloned_repo = context().cloned_repo
    image_registry_url = context.get_protocol_free_image_registry_url()

    latest_commit_hash = cloned_repo.head.commit.hexsha

    repo_url = cloned_repo.remotes.origin.url
    user_repo_name = repo_url.split("github.com/")[1].split(".git")[0]
    # Note: (docker) image registry URLs do now allow upper cases.
    username = user_repo_name.split("/")[0].lower()
    repo_name = user_repo_name.split("/")[1]

    context().set_new_image_name_prefix(f"{image_registry_url}/{username}/{repo_name}")
    context().set_new_image_tag(latest_commit_hash)


def _push_images(context: ContextFLActors) -> None:
    context.timer.start_new_time_frame(IMAGE_PUSH_TIMEFRAME)
    push_image(context.get_learner_image_name())
    push_image(context.get_aggregator_image_name())
    context.timer.end_time_frame(IMAGE_PUSH_TIMEFRAME)


def _build_base_image(context: ContextFLActors) -> None:
    context.timer.start_new_time_frame(BASE_IMAGE_BUILD_TIMEFRAME)
    if context.use_devel_base_images:
        build_image(
            build_directory=FL_BASE_IMAGE_PATH,
            is_flops_base_image=True,
            base_image_to_use=DEVEL_BASE_IMAGES_MAPPING[context.repo_url],
        )
    else:
        build_image(build_directory=FL_BASE_IMAGE_PATH, is_flops_base_image=True)

    context.timer.end_time_frame(BASE_IMAGE_BUILD_TIMEFRAME)


def _build_fl_actor_images(context: ContextFLActors) -> None:
    context.timer.start_new_time_frame(BUILD_ALL_IMAGES_TIMEFRAME)

    _build_base_image()

    build_image(
        build_directory=FL_LEARNER_IMAGE_PATH,
        image_name_with_tag=context.get_learner_image_name(),
        base_image_to_use=_FL_BASE_IMAGE_NAME,
    )

    build_image(
        build_directory=FL_AGGREGATOR_IMAGE_PATH,
        image_name_with_tag=context.get_aggregator_image_name(),
        base_image_to_use=_FL_BASE_IMAGE_NAME,
    )
    context.timer.end_time_frame(BUILD_ALL_IMAGES_TIMEFRAME)


def handle_fl_actor_images_build(context: ContextFLActors) -> None:
    context.timer.start_new_time_frame(BUILD_PREPARATION_TIMEFRAME)
    clone_repo()
    check_cloned_repo()
    _prepare_new_image_names(context)
    context.timer.end_time_frame(BUILD_PREPARATION_TIMEFRAME)
    _build_fl_actor_images(context)
    _push_images()
