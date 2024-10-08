#!/usr/bin/env python3
from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING

import mlflow
from flops_utils.logging import logger
from flops_utils.shell import run_in_shell
from utils.timeframes import BUILD_PREPARATION_TIMEFRAME

if TYPE_CHECKING:
    from context.trained_model import ContextTrainedModel

from build_plans.trained_model.common import DOCKERFILE_DIR

# NOTE: Currently max only one model is logged/saved per MLflow run.
# It is mandatory to provide a name when logging models.
# For simplicity sake we use the same.
MODEL_ARTIFACT_NAME = "logged_model_artifact"
DOWNLOADED_MODEL_DIR = pathlib.Path("downloaded_model")
MODEL_URI = DOWNLOADED_MODEL_DIR / MODEL_ARTIFACT_NAME


def _augment_dockerfile() -> None:
    """The MLflow created Dockerfile is not capable to be used
    for multi-platform (especially ARM) builds.
    We augment it to enable multi-platform support."""

    DOCKERFILE_PATH = DOCKERFILE_DIR / "Dockerfile"
    with open(DOCKERFILE_PATH, "r") as file:
        dockerfile_lines = file.readlines()

    from_index = None
    for i, line in enumerate(dockerfile_lines):
        if line.strip().startswith("FROM"):
            from_index = i
            break

    assert from_index
    multi_platform_fix = " ".join(
        (
            "RUN",
            "apt-get update",
            "&& apt-get install -y",
            "gcc python3-dev",
            "&& apt-get clean",
        )
    )
    dockerfile_lines.insert(from_index + 1, f"\n{multi_platform_fix}\n")
    with open(DOCKERFILE_PATH, "w") as file:
        file.writelines(dockerfile_lines)


def _create_dockerfile() -> None:
    shell_cmd = " ".join(
        (
            "mlflow models generate-dockerfile",
            f"--model-uri {MODEL_URI}",
            f"--output-directory {DOCKERFILE_DIR}",
        )
    )
    # NOTE: We have to run this cmd via shell because there is no equivalent python API yet.
    run_in_shell(shell_cmd=shell_cmd)
    _augment_dockerfile()


def _prepare_new_image_name(context: ContextTrainedModel) -> None:
    # NOTE: (docker) image registry URLs do now allow upper cases.
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
        dst_path=DOWNLOADED_MODEL_DIR,  # type: ignore
    )
    logger.debug("Downloaded model artifact directory")
    # NOTE: We first build a dockerfile and then based on it the image via buildah.
    # MLflow has a command for building the image directly but it uses docker for it.
    _create_dockerfile()
    logger.debug("Created dockerfile")
    _prepare_new_image_name(context=context)
    context.timer.end_time_frame(BUILD_PREPARATION_TIMEFRAME)
