from __future__ import annotations

from typing import TYPE_CHECKING

from build_plans.fl_actors.images.devel_base_images import DEVEL_BASE_IMAGES_MAPPING
from build_plans.fl_actors.paths import (
    FL_AGGREGATOR_IMAGE_PATH,
    FL_BASE_IMAGE_PATH,
    FL_LEARNER_IMAGE_PATH,
)
from image_management import build_image
from utils.timeframes import ACTOR_IMAGES_BUILD_TIMEFRAME, BASE_IMAGE_BUILD_TIMEFRAME

if TYPE_CHECKING:
    from context.fl_actors import ContextFLActors


def build_base_image(context: ContextFLActors) -> None:
    context.timer.start_new_time_frame(BASE_IMAGE_BUILD_TIMEFRAME)
    _build_fl_actor_image(
        context=context,
        build_directory=FL_BASE_IMAGE_PATH,  # type: ignore
        image_name_with_tag=context.get_base_image_name(),
        is_flops_base_image=True,
        base_image_to_use=(
            DEVEL_BASE_IMAGES_MAPPING[context.repo_url] if context.use_devel_base_images else ""
        ),
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
    context.timer.start_new_time_frame(ACTOR_IMAGES_BUILD_TIMEFRAME)
    # NOTE: Using the following base-image approach works great for
    # images with only a single target architecture.
    # Once you use multiple --platforms or even the --all-platforms flags
    # errors show up if the base-image is only available locally,
    # i.e. if the base image was not yet pushed to a registry.
    #
    # Let's compare this with building multi-platform images with docker.
    # In docker to do so nicely one uses buildx.
    # When building a single image that supports multiple platforms
    # one has to push it immediately (AFAIK), because the local machine
    # can only work with a single architecture. (A subset of all layers.)
    #
    # The failure reason seems to be the following when doing this via buildah:
    # When building a multi-platform image we do not automatically push it (AFAIK).
    # When using it as a base-image the builder expects to get a subset of layers
    # intended for the specific platform.
    # E.g. when building the learner image for linux/arm64
    # the fl_base image layers for linux/arm64 should be used.
    # But buildah fails to locate the just-build fl_base image entirely.
    # Even when specifying the FQDN that points to the local machine.
    # Using/Creating manifest files also does not help.
    #
    # There seems to be three solutions for this:
    # 1) Be/Become an expert in niche docker/buildah concepts and figure out the proper way.
    # -> Very time consuming.
    # 2) Push the intermediate fl_base base-image to the FLOps registry
    # -> Very resource wasteful. (Push/Store an intermediate image and pull it again.)
    # 3) Do not use base-images for multi-platform images.
    # -> The Dockerfiles for the Aggregator and Learner will contain shared init layers.
    # -> These layers should be reusable by the builder and registry because they are identical.

    _build_fl_actor_image(
        context=context,
        build_directory=FL_LEARNER_IMAGE_PATH,  # type: ignore
        image_name_with_tag=context.get_learner_image_name(),
        base_image_to_use=context.get_base_image_name(),
    )
    _build_fl_actor_image(
        context=context,
        build_directory=FL_AGGREGATOR_IMAGE_PATH,  # type: ignore
        image_name_with_tag=context.get_aggregator_image_name(),
        base_image_to_use=context.get_base_image_name(),
    )
    context.timer.end_time_frame(ACTOR_IMAGES_BUILD_TIMEFRAME)
