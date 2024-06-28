from typing import Dict, List, Optional, Tuple, Union

import flwr as fl
import mlflow
import numpy as np
from flops_utils.ml_repo_files_proxy import get_model_manager
from flwr.common import (
    EvaluateRes,
    FitIns,
    FitRes,
    Parameters,
    Scalar,
    parameters_to_ndarrays,
)
from flwr.server.client_manager import ClientManager
from flwr.server.client_proxy import ClientProxy
from flwr.server.strategy.aggregate import weighted_loss_avg
from strategies.logging import (
    handle_system_metrics_logging,
    init_logging,
    log_project_params,
)
from strategies.model_tracking import handle_model_tracking
from utils.aggregator_context import AggregatorContext


class FLOpsFedAvg(fl.server.strategy.FedAvg):
    def __init__(
        self,
        aggregator_context: AggregatorContext,
        mlflow_experiment_id: Optional[int],
        requested_total_number_of_training_rounds: int,
        *args,
        **kwargs,
    ):
        self.aggregator_context = aggregator_context
        if self.aggregator_context.should_use_mlflow:
            init_logging()
        self.mlflow_experiment_id = mlflow_experiment_id
        self.requested_total_number_of_training_rounds = (
            requested_total_number_of_training_rounds
        )
        self.model_manager = get_model_manager()
        # NOTE: Both will be overwritten after the first training round.
        self.best_found_accuracy = -1
        self.best_found_loss = -1
        super().__init__(*args, **kwargs)

    def configure_fit(
        self,
        server_round: int,
        parameters: Parameters,
        client_manager: ClientManager,
    ) -> List[Tuple[ClientProxy, FitIns]]:
        if self.aggregator_context.should_use_mlflow:
            if mlflow.active_run():
                mlflow.end_run()
            mlflow.start_run(
                experiment_id=self.mlflow_experiment_id,  # type: ignore
                run_name=f"FLOps FL round {server_round}",
            )
            log_project_params(strategy=self)
        return super().configure_fit(server_round, parameters, client_manager)

    def aggregate_fit(
        self,
        server_round: int,
        results: List[Tuple[ClientProxy, FitRes]],
        failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]],
    ) -> Tuple[Optional[Parameters], Dict[str, Scalar]]:
        parameters_aggregated, metrics_aggregated = super().aggregate_fit(
            server_round, results, failures
        )

        if parameters_aggregated is not None:
            aggregated_ndarrays: List[np.ndarray] = parameters_to_ndarrays(
                parameters_aggregated
            )
            self.model_manager.set_model_parameters(aggregated_ndarrays)

        return parameters_aggregated, metrics_aggregated

    def aggregate_evaluate(
        self,
        server_round: int,
        results: List[Tuple[ClientProxy, EvaluateRes]],
        failures: List[Union[Tuple[ClientProxy, EvaluateRes], BaseException]],
    ) -> Tuple[Optional[float], Dict[str, Scalar]]:
        """Aggregate evaluation losses and accuracy using weighted average."""

        if not results:
            return None, {}

        loss_aggregated = weighted_loss_avg(
            [
                (evaluate_res.num_examples, evaluate_res.loss)
                for _, evaluate_res in results
            ]
        )
        accuracies = [
            evaluate_res.metrics["accuracy"] * evaluate_res.num_examples
            for _, evaluate_res in results
        ]
        examples = [evaluate_res.num_examples for _, evaluate_res in results]
        accuracy_aggregated = (
            sum(accuracies) / sum(examples) if sum(examples) != 0 else 0  # type: ignore
        )

        metrics_aggregated = {"loss": loss_aggregated, "accuracy": accuracy_aggregated}
        if self.aggregator_context.should_use_mlflow:
            mlflow.log_metrics(metrics_aggregated)
        handle_model_tracking(
            strategy=self,
            server_round=server_round,
            current_rounds_accuracy=accuracy_aggregated,
            current_rounds_loss=loss_aggregated,
            should_use_mlflow=self.aggregator_context.should_use_mlflow,
        )
        if self.aggregator_context.should_use_mlflow:
            mlflow.end_run()
            handle_system_metrics_logging()
        return loss_aggregated, metrics_aggregated
