from __future__ import annotations

from typing import TYPE_CHECKING

from build_plans.fl_actors.images.devel_base_images import DEVEL_BASE_IMAGES_MAPPING
from build_plans.fl_actors.paths import (
    FL_AGGREGATOR_IMAGE_PATH,
    FL_BASE_IMAGE_PATH,
    FL_LEARNER_IMAGE_PATH,
)
from image_management import build_image
from utils.timeframes import BASE_IMAGE_BUILD_TIMEFRAME, BUILD_ALL_IMAGES_TIMEFRAME

if TYPE_CHECKING:
    from context.fl_actors import ContextFLActors

_FL_BASE_IMAGE_NAME = "fl_base"


def _build_base_image(context: ContextFLActors) -> None:
    context.timer.start_new_time_frame(BASE_IMAGE_BUILD_TIMEFRAME)
    if context.use_devel_base_images:
        _build_fl_actor_image(
            context=context,
            build_directory=FL_BASE_IMAGE_PATH,  # type: ignore
            is_flops_base_image=True,
            base_image_to_use=DEVEL_BASE_IMAGES_MAPPING[context.repo_url],
        )
    else:
        _build_fl_actor_image(
            context=context,
            build_directory=FL_BASE_IMAGE_PATH,  # type: ignore
            is_flops_base_image=True,
        )

    context.timer.end_time_frame(BASE_IMAGE_BUILD_TIMEFRAME)


def _build_fl_actor_image(
    context: ContextFLActors,
    build_directory: str,
    image_name_with_tag: str = "",
    base_image_to_use: str = "",
    is_flops_base_image: bool = False,
) -> None:
    build_cmd_addition = ""
    if is_flops_base_image:
        model_flavor = context.ml_model_flavor.value
        build_cmd_addition += f" --build-arg ML_MODEL_FLAVOR={model_flavor}"
        if context.use_devel_base_images:
            build_cmd_addition += " -f devel.Dockerfile"
    if base_image_to_use:
        build_cmd_addition += f" --build-arg BASE_IMAGE={base_image_to_use}"
        if context.use_devel_base_images:
            build_cmd_addition += f" --build-arg USE_DEVEL_BASE_IMAGES={True}"
    build_image(
        context=context,
        build_directory=build_directory,
        image_name_with_tag=image_name_with_tag,
        base_image_to_use=base_image_to_use,
        should_notify_observer=is_flops_base_image,
        build_cmd_addition=build_cmd_addition,
    )


def build_fl_actor_images(context: ContextFLActors) -> None:
    context.timer.start_new_time_frame(BUILD_ALL_IMAGES_TIMEFRAME)
    _build_base_image(context=context)
    _build_fl_actor_image(
        context=context,
        build_directory=FL_LEARNER_IMAGE_PATH,  # type: ignore
        image_name_with_tag=context.get_learner_image_name(),
        base_image_to_use=_FL_BASE_IMAGE_NAME,
    )
    _build_fl_actor_image(
        context=context,
        build_directory=FL_AGGREGATOR_IMAGE_PATH,  # type: ignore
        image_name_with_tag=context.get_aggregator_image_name(),
        base_image_to_use=_FL_BASE_IMAGE_NAME,
    )
    context.timer.end_time_frame(BUILD_ALL_IMAGES_TIMEFRAME)
