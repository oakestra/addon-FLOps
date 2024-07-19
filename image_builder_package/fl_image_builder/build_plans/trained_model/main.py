#!/usr/bin/env python3
from __future__ import annotations

from typing import TYPE_CHECKING

from build_plans.trained_model.common import DOCKERFILE_DIR
from build_plans.trained_model.preparations import prepare_build
from flops_utils.logging import logger
from image_management import build_image, push_image
from utils.timeframes import (
    BUILD_IMAGE_TIMEFRAME,
    FULL_BUILDER_PROCESS_TIMEFRAME,
    PUSH_IMAGE_TIMEFRAME,
)

if TYPE_CHECKING:
    from context.trained_model import ContextTrainedModel


def handle_trained_model_image_build(context: ContextTrainedModel) -> None:
    context.timer.start_new_time_frame(FULL_BUILDER_PROCESS_TIMEFRAME)
    logger.debug("Start handling trained model image build process")
    try:
        prepare_build(context=context)

        context.timer.start_new_time_frame(BUILD_IMAGE_TIMEFRAME)
        build_image(
            context=context,
            build_directory=DOCKERFILE_DIR,  # type: ignore
            image_name_with_tag=context.get_image_name(),
            should_notify_observer=True,
        )
        context.timer.end_time_frame(BUILD_IMAGE_TIMEFRAME)

        context.timer.start_new_time_frame(PUSH_IMAGE_TIMEFRAME)
        push_image(context=context)
        context.timer.end_time_frame(PUSH_IMAGE_TIMEFRAME)
    except Exception as e:
        msg = "Something unexpected went wrong"
        logger.exception(msg)
        context.notify_about_failed_build_and_terminate(f"{msg}; '{e}'")

    context.timer.end_time_frame(FULL_BUILDER_PROCESS_TIMEFRAME)
    context.notify_about_successful_builder_process()
