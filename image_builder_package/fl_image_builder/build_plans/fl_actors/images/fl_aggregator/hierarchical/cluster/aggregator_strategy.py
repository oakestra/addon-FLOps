# from typing import Dict, List, Optional, Tuple, Union

# import flwr as fl
# import numpy as np
# from flops_utils.ml_repo_files_proxy import get_model_manager
# from flwr.common import (
#     EvaluateRes,
#     FitIns,
#     FitRes,
#     Parameters,
#     Scalar,
#     parameters_to_ndarrays,
# )
# from flwr.server.client_manager import ClientManager
# from flwr.server.client_proxy import ClientProxy
# from flwr.server.strategy.aggregate import weighted_loss_avg
# from utils.aggregator_context import AggregatorContext


# # NOTE:
# # For now the Cluster Aggregator (CAg) does not use MLflow
# # i.e. it does not log or track anything. Only the Root Aggregator does so.
# # This is done for simplicity and privacy reasons.
# #
# # The CAg needs to perform a classic FL training round with learners in its cluster.
# # At the end of each round the CAg needs to act as a learner and forward its
# # aggregated trained model weights to the Root Aggregator.
# class FLOpsHierarchicalCluster(fl.server.strategy.FedAvg):
#     def __init__(
#         self,
#         aggregator_context: AggregatorContext,
#         requested_total_number_of_training_rounds: int,
#         *args,
#         **kwargs,
#     ):
#         self.aggregator_context = aggregator_context
#         self.requested_total_number_of_training_rounds = (
#             requested_total_number_of_training_rounds
#         )
#         self.model_manager = get_model_manager()
#         # NOTE: Both will be overwritten after the first training round.
#         self.best_found_accuracy = -1
#         self.best_found_loss = -1
#         super().__init__(*args, **kwargs)

#     def configure_fit(
#         self,
#         server_round: int,
#         parameters: Parameters,
#         client_manager: ClientManager,
#     ) -> List[Tuple[ClientProxy, FitIns]]:
#         return super().configure_fit(server_round, parameters, client_manager)

#     def aggregate_fit(
#         self,
#         server_round: int,
#         results: List[Tuple[ClientProxy, FitRes]],
#         failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]],
#     ) -> Tuple[Optional[Parameters], Dict[str, Scalar]]:
#         parameters_aggregated, metrics_aggregated = super().aggregate_fit(
#             server_round, results, failures
#         )

#         if parameters_aggregated is not None:
#             aggregated_ndarrays: List[np.ndarray] = parameters_to_ndarrays(
#                 parameters_aggregated
#             )
#             self.model_manager.set_model_parameters(aggregated_ndarrays)

#         return parameters_aggregated, metrics_aggregated

#     def aggregate_evaluate(
#         self,
#         server_round: int,
#         results: List[Tuple[ClientProxy, EvaluateRes]],
#         failures: List[Union[Tuple[ClientProxy, EvaluateRes], BaseException]],
#     ) -> Tuple[Optional[float], Dict[str, Scalar]]:
#         """Aggregate evaluation losses and accuracy using weighted average."""

#         if not results:
#             return None, {}

#         loss_aggregated = weighted_loss_avg(
#             [
#                 (evaluate_res.num_examples, evaluate_res.loss)
#                 for _, evaluate_res in results
#             ]
#         )
#         accuracies = [
#             evaluate_res.metrics["accuracy"] * evaluate_res.num_examples
#             for _, evaluate_res in results
#         ]
#         examples = [evaluate_res.num_examples for _, evaluate_res in results]
#         accuracy_aggregated = (
#             sum(accuracies) / sum(examples) if sum(examples) != 0 else 0
#         )

#         metrics_aggregated = {"loss": loss_aggregated, "accuracy": accuracy_aggregated}
#         return loss_aggregated, metrics_aggregated
