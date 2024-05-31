#!/usr/bin/env python3
from __future__ import annotations

from typing import TYPE_CHECKING

import mlflow
from flops_utils.logging import logger
from repo_management import check_cloned_repo, clone_repo
from utils.timeframes import BUILD_PREPARATION_TIMEFRAME

if TYPE_CHECKING:
    from context.trained_model import ContextTrainedModel


def download_trained_model(context: ContextTrainedModel) -> None:
    mlflow.artifacts.download_artifacts(
        # TODO inject param here
        run_id=context.run_id,
        artifact_path="logged_model_artifact",
        dst_path="trained_model",
    )


def build_trained_model_image(context: ContextTrainedModel) -> None:
    logger.debug("0" * 15)
    context.timer.start_new_time_frame(BUILD_PREPARATION_TIMEFRAME)
    # TODO add tracking server URI as param to builder (only needed for trained model build plan not the normal one!)
    mlflow.set_tracking_uri("http://192.168.178.44:7027")
    # clone_repo()
    logger.debug("1" * 15)
    download_trained_model(context)
    logger.debug("2" * 15)
    # prepare_new_image_names()
    # context.timer.end_time_frame(BUILD_PREPARATION_TIMEFRAME)
    # build_trained_model_image()
    # push_image()
