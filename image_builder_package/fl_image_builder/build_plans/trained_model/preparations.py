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

from build_plans.trained_model.common import DOCKERFILE_DIR

# Note: Currently max only one model is logged/saved per MLflow run.
# It is mandatory to provide a name when logging models.
# For simplicity sake we use the same.
MODEL_ARTIFACT_NAME = "logged_model_artifact"
DOWNLOADED_MODEL_DIR = pathlib.Path("downloaded_model")


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
    image_registry_url = context.get_protocol_free_image_registry_url()
    context.set_new_image_name_prefix(
        f"{image_registry_url}/{context.customer_id.lower()}/trained_model"
    )
    context.set_new_image_tag(context.run_id)


def prepare_build(context: ContextTrainedModel) -> None:
    context.timer.start_new_time_frame(BUILD_PREPARATION_TIMEFRAME)
    mlflow.set_tracking_uri(context.tracking_server_uri)
    mlflow.artifacts.download_artifacts(
        run_id=context.run_id,
        artifact_path=MODEL_ARTIFACT_NAME,
        dst_path=DOWNLOADED_MODEL_DIR,
    )
    logger.debug("Downloaded model artifact directory")
    # Note: We first build a dockerfile and then based on it the image via buildah.
    # MLflow has a command for building the image directly but it uses docker for it.
    _create_dockerfile()
    logger.debug("Created dockerfile")
    _prepare_new_image_name(context=context)
    context.timer.end_time_frame(BUILD_PREPARATION_TIMEFRAME)
