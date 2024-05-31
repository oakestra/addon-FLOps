#!/usr/bin/env python3
from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

import mlflow
from flops_utils.logging import logger
from utils.common import run_in_bash
from utils.timeframes import BUILD_PREPARATION_TIMEFRAME

if TYPE_CHECKING:
    from context.trained_model import ContextTrainedModel

# Note: Currently max only one model is logged/saved per MLflow run.
# It is mandatory to provide a name when logging models.
# For simplicity sake we use the same.
MODEL_ARTIFACT_NAME = "logged_model_artifact"
DOWNLOADED_MODEL_DIR = pathlib.Path("downloaded_model")
DOCKERFILE_DIR = pathlib.Path("trained_model_dockerfile_dir")


def _download_trained_model(context: ContextTrainedModel) -> None:
    mlflow.artifacts.download_artifacts(
        run_id=context.run_id,
        artifact_path=MODEL_ARTIFACT_NAME,
        dst_path=DOWNLOADED_MODEL_DIR,
    )


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


def handle_trained_model_image_build(context: ContextTrainedModel) -> None:
    context.timer.start_new_time_frame(BUILD_PREPARATION_TIMEFRAME)
    # TODO add tracking server URI as param to builder
    # (only needed for trained model build plan not the normal one!)
    mlflow.set_tracking_uri("http://192.168.178.44:7027")
    _download_trained_model(context)
    # Note: We first build a dockerfile and then based on it the image via buildah.
    # MLflow has a command for building the image directly but it uses docker for it.
    _create_dockerfile()
    # prepare_new_image_names()
    # context.timer.end_time_frame(BUILD_PREPARATION_TIMEFRAME)
    # build_trained_model_image()
    # push_image()
