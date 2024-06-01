#!/usr/bin/env python3
from __future__ import annotations

from typing import TYPE_CHECKING

from build_plans.fl_actors.builds import build_fl_actor_images
from build_plans.fl_actors.repo_management import check_cloned_repo, clone_repo
from flops_utils.logging import logger
from image_management import push_image
from utils.timeframes import (
    BUILD_PREPARATION_TIMEFRAME,
    FULL_BUILDER_PROCESS_TIMEFRAME,
    IMAGE_PUSH_TIMEFRAME,
)

if TYPE_CHECKING:
    from context.fl_actors import ContextFLActors


def _prepare_new_image_names(context: ContextFLActors) -> None:
    cloned_repo = context.cloned_repo
    image_registry_url = context.get_protocol_free_image_registry_url()

    latest_commit_hash = cloned_repo.head.commit.hexsha

    repo_url = cloned_repo.remotes.origin.url
    user_repo_name = repo_url.split("github.com/")[1].split(".git")[0]
    # Note: (docker) image registry URLs do now allow upper cases.
    username = user_repo_name.split("/")[0].lower()
    repo_name = user_repo_name.split("/")[1]

    context.set_new_image_name_prefix(f"{image_registry_url}/{username}/{repo_name}")
    context.set_new_image_tag(latest_commit_hash)


def handle_fl_actor_images_build(context: ContextFLActors) -> None:
    context.timer.start_new_time_frame(FULL_BUILDER_PROCESS_TIMEFRAME)
    try:
        context.timer.start_new_time_frame(BUILD_PREPARATION_TIMEFRAME)
        clone_repo(context=context)
        check_cloned_repo(context=context)
        _prepare_new_image_names(context)
        context.timer.end_time_frame(BUILD_PREPARATION_TIMEFRAME)

        build_fl_actor_images(context)

        context.timer.start_new_time_frame(IMAGE_PUSH_TIMEFRAME)
        push_image(
            context=context,
            image_name_with_tag=context.get_learner_image_name(),
        )
        push_image(
            context=context,
            image_name_with_tag=context.get_aggregator_image_name(),
        )
        context.timer.end_time_frame(IMAGE_PUSH_TIMEFRAME)
    except Exception as e:
        msg = "Something unexpected went wrong"
        logger.exception(msg)
        context.notify_about_failed_build_and_terminate(f"{msg}; '{e}'")

    context.timer.end_time_frame(FULL_BUILDER_PROCESS_TIMEFRAME)
    context.notify_about_successful_builder_process()
