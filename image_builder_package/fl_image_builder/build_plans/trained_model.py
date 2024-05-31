#!/usr/bin/env python3
from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

import mlflow
from flops_utils.logging import logger
from image_management import build_image, push_image
from utils.common import run_in_bash
from utils.timeframes import (
    BUILD_IMAGE_TIMEFRAME,
    BUILD_PREPARATION_TIMEFRAME,
    IMAGE_PUSH_TIMEFRAME,
)

if TYPE_CHECKING:
    from context.trained_model import ContextTrainedModel

# Note: Currently max only one model is logged/saved per MLflow run.
# It is mandatory to provide a name when logging models.
# For simplicity sake we use the same.
MODEL_ARTIFACT_NAME = "logged_model_artifact"
DOWNLOADED_MODEL_DIR = pathlib.Path("downloaded_model")
DOCKERFILE_DIR = pathlib.Path("trained_model_dockerfile_dir")


def _create_dockerfile() -> None:
    # Note: We have to run this cmd via shell because there is no equivalent python API yet.
    run_in_bash(
        bash_cmd=" ".join(
            (
                "mlflow models generate-dockerfile",
                f"--model-uri {DOWNLOADED_MODEL_DIR}/{MODEL_ARTIFACT_NAME}",
                f"--output-directory {DOCKERFILE_DIR}",
            )
        )
    )


def _prepare_new_image_name(context: ContextTrainedModel) -> None:
    # Note: (docker) image registry URLs do now allow upper cases.
    # TODO inject customer_id here
    # username = customer_id
    customer_id = "Admin"
    image_registry_url = context.get_protocol_free_image_registry_url()
    context().set_new_image_name_prefix(
        f"{image_registry_url}/{customer_id}/trained_model"
    )
    context().set_new_image_tag(context.run_id)


def handle_trained_model_image_build(context: ContextTrainedModel) -> None:
    context.timer.start_new_time_frame(BUILD_PREPARATION_TIMEFRAME)
    # TODO add tracking server URI as param to builder
    # (only needed for trained model build plan not the normal one!)
    mlflow.set_tracking_uri("http://192.168.178.44:7027")
    mlflow.artifacts.download_artifacts(
        run_id=context.run_id,
        artifact_path=MODEL_ARTIFACT_NAME,
        dst_path=DOWNLOADED_MODEL_DIR,
    )
    # Note: We first build a dockerfile and then based on it the image via buildah.
    # MLflow has a command for building the image directly but it uses docker for it.
    _create_dockerfile()
    _prepare_new_image_name()
    context.timer.end_time_frame(BUILD_PREPARATION_TIMEFRAME)
    context.timer.start_new_time_frame(BUILD_IMAGE_TIMEFRAME)
    build_image(
        build_directory=DOCKERFILE_DIR,
        image_name_with_tag=context.get_image_name(),
    )
    context.timer.end_time_frame(BUILD_IMAGE_TIMEFRAME)
    context.timer.start_new_time_frame(IMAGE_PUSH_TIMEFRAME)
    push_image(context.get_image_name())
    context.timer.end_time_frame(IMAGE_PUSH_TIMEFRAME)
