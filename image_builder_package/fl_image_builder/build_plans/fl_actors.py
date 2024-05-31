#!/usr/bin/env python3
from __future__ import annotations

from typing import TYPE_CHECKING

from image_management import build_fl_actor_images, prepare_new_image_names, push_images
from repo_management import check_cloned_repo, clone_repo
from utils.timeframes import BUILD_PREPARATION_TIMEFRAME

if TYPE_CHECKING:
    from context.fl_actors import ContextFLActors


def build_fl_actor_images(context: ContextFLActors) -> None:
    context.timer.start_new_time_frame(BUILD_PREPARATION_TIMEFRAME)
    clone_repo()
    check_cloned_repo()
    prepare_new_image_names()
    context.timer.end_time_frame(BUILD_PREPARATION_TIMEFRAME)
    build_fl_actor_images()
    push_images()
