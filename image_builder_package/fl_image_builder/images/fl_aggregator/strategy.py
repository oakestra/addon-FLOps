from typing import Dict, List, Optional, Tuple, Union

import flwr as fl
import mlflow
import numpy as np
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

# Note: This is part of the "to-be" injected client ML repo.
from model_manager import ModelManager
from prometheus_client import Gauge
from utils.ml_model_flavor_wrapper import mlflow_model_flavor


class OakFedAvg(fl.server.strategy.FedAvg):
    def __init__(
        self,
        mlflow_experiment_id: int,
        accuracy_gauge: Gauge = None,
        loss_gauge: Gauge = None,
        *args,
        **kwargs,
    ):
        self.mlflow_experiment_id = mlflow_experiment_id
        self.model_manager = ModelManager()

        super().__init__(*args, **kwargs)

        self.accuracy_gauge = accuracy_gauge
        self.loss_gauge = loss_gauge

    def _log_project_params(self):
        interesting_params = [
            "min_available_clients",
            "min_evaluate_clients",
            "min_fit_clients",
            "fraction_evaluate",
            "fraction_fit",
            # "global_parameters",
            # "initial_parameters",
        ]

        mlflow.log_params(
            dict(
                filter(
                    lambda pair: pair[0] in interesting_params, list(vars(self).items())
                )
            )
        )

    def configure_fit(
        self, server_round: int, parameters: Parameters, client_manager: ClientManager
    ) -> List[Tuple[ClientProxy, FitIns]]:
        if mlflow.active_run():
            mlflow.end_run()
        mlflow.start_run(
            experiment_id=self.mlflow_experiment_id,
            run_name=f"FLOps FL round {server_round}",
            # log_system_metrics=True, # TODO + pip install pynvml & psutils
        )
        self._log_project_params()
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
            mlflow_model_flavor.log_model(
                self.model_manager.get_model(), "alex_model_testing"
            )

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

        # Calculate weighted average for loss using the provided function
        loss_aggregated = weighted_loss_avg(
            [
                (evaluate_res.num_examples, evaluate_res.loss)
                for _, evaluate_res in results
            ]
        )

        # Calculate weighted average for accuracy
        accuracies = [
            evaluate_res.metrics["accuracy"] * evaluate_res.num_examples
            for _, evaluate_res in results
        ]
        examples = [evaluate_res.num_examples for _, evaluate_res in results]
        accuracy_aggregated = (
            sum(accuracies) / sum(examples) if sum(examples) != 0 else 0
        )

        # Update the Prometheus gauges with the latest aggregated accuracy and loss values
        self.accuracy_gauge.set(accuracy_aggregated)
        self.loss_gauge.set(loss_aggregated)

        metrics_aggregated = {"loss": loss_aggregated, "accuracy": accuracy_aggregated}

        mlflow.log_metrics(metrics_aggregated)
        mlflow.end_run()
        return loss_aggregated, metrics_aggregated
