from __future__ import annotations

import pathlib
import shutil
from typing import TYPE_CHECKING

import mlflow
from flops_utils.ml_model_flavor_proxy import get_ml_model_flavor
from utils.aggregator_context import WinnerModel

if TYPE_CHECKING:
    from strategy.main import FLOpsFedAvg


TRACKED_MODEL_NAME = "logged_model_artifact"
TRACKED_MODEL_DIR = pathlib.Path(TRACKED_MODEL_NAME)


def handle_model_tracking(
    strategy: FLOpsFedAvg,
    server_round: int,
    current_rounds_accuracy: float,
    current_rounds_loss: float,
) -> None:

    def update_best_found_model():
        strategy.best_found_accuracy = current_rounds_accuracy
        strategy.best_found_loss = current_rounds_loss
        if TRACKED_MODEL_DIR.exists():
            shutil.rmtree(TRACKED_MODEL_DIR)
        # This saves the current model locally.
        get_ml_model_flavor().save_model(strategy.model_manager.get_model(), TRACKED_MODEL_DIR)

    if server_round == 1:
        update_best_found_model()
        return

    if (
        current_rounds_accuracy > strategy.best_found_accuracy
        and current_rounds_loss < strategy.best_found_loss
    ):
        update_best_found_model()

    # Note: Only log the best found model after the last training round.
    # Logging means sending the model data to the remote artifact store.
    if server_round == strategy.requested_total_number_of_training_rounds:
        get_ml_model_flavor().log_model(
            get_ml_model_flavor().load_model(TRACKED_MODEL_DIR),
            TRACKED_MODEL_NAME,
        )
        # Update the aggregator context to be able to inform the project observer in the end.
        current_run = mlflow.active_run()
        strategy.aggregator_context.winner_model = WinnerModel(
            accuracy=strategy.best_found_accuracy,
            loss=strategy.best_found_loss,
            experiment_id=current_run.info.experiment_id,
            run_id=current_run.info.run_id,
        )
