import time
from typing import Dict, List, Optional, Tuple, Union

import flwr as fl
import mlflow
import numpy as np
from flops_utils.logging import logger
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
        model_manager,
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
        self.model_manager = model_manager
        # NOTE: Both will be overwritten after the first training round.
        self.best_found_accuracy = -1
        self.best_found_loss = -1

        self.current_cycles_number_of_training_examples = 0
        self.current_cycles_number_of_evaluation_examples = 0
        # NOTE: The CAg will send the RAg only a single value for loss and accuracy.
        # To find this value out, the CAg collects all losses and accuracies.
        # One per training round.
        # When sending a response to the RAg, the average of these values will be used.
        self.current_cycles_losses = []
        self.current_cycles_accuracies = []
        super().__init__(*args, **kwargs)

    def configure_fit(
        self,
        server_round: int,
        parameters: Parameters,
        client_manager: ClientManager,
    ) -> List[Tuple[ClientProxy, FitIns]]:
        if server_round == 1:
            # NOTE:
            # In the case of HFL the strategy gets reused to continue to improve the model.
            # All training rounds of a CAg equal a single training round/cycle for the RAg.
            # We aggregate all seen examples during a CAg training to send the result to the RAg.
            # Once the next cycle starts we reuse the strategy to keep improving the same model,
            # so we need to reset the aggregated auxiliary variables.
            #
            # Example to demonstrate this need.
            # Let's say we have 3 cycles with 5 rounds each.
            # We assume a trivial case with just a single cluster - 1 CAg.
            # During the first cycle we perform 5 training rounds, per round we see 100 examples.
            # The cycle has seen 500 example. This number needs to be send to the RAg by the CAg.
            # The next cycle starts, we need to reset the 500,
            # otherwise we suddenly would see that the second RAg cycle
            # had twice as many examples as the last once, which is wrong.
            self.current_cycles_number_of_training_examples = 0
            self.current_cycles_number_of_evaluation_examples = 0
            self.current_cycles_losses = []
            self.current_cycles_accuracies = []

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

        for result_tuple in results:
            fit_res_object = result_tuple[1]
            num_examples = fit_res_object.num_examples
            self.current_cycles_number_of_training_examples += num_examples

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

        # NOTE: The examples, aggregated loss & accuracy need to be forwarded
        # to the Root Aggregator if this is a case of hierarchical FL.
        # NOTE:'examples' are a list of num_examples, e.g. [12000, 12000]
        self.current_cycles_number_of_evaluation_examples += sum(examples)
        self.current_cycles_losses.append(loss_aggregated)
        self.current_cycles_accuracies.append(accuracy_aggregated)

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
