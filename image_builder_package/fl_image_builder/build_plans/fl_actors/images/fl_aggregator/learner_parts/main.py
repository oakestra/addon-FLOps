# import time
# from typing import Any

# import flwr
# from context import get_context
# from flops_utils.logging import logger
# from model_manager import get_model_manager

# # I have a feeling that for this to work the CAg first needs to be
# # started as a "Learner" for the RAg and only afterwards
# # (starting with the init param gathering) start its own aggregation things.


# class ClusterAggregatorAsLearner(flwr.client.NumPyClient):

#     def __init__(self):
#         self.model_manager = get_model_manager()
#         self.model_manager.set_model_data()

#     def get_parameters(self, config=None) -> Any:
#         return self.model_manager.get_model_parameters()

#     def set_parameters(self, parameters) -> None:
#         self.model_manager.set_model_parameters(parameters)

#     def fit(self, parameters, config):
#         self.set_parameters(parameters)
#         number_of_training_examples = self.model_manager.fit_model()
#         return self.get_parameters(), number_of_training_examples, {}

#     def evaluate(self, parameters, config):
#         self.set_parameters(parameters)
#         loss, accuracy, number_of_evaluation_examples = (
#             self.model_manager.evaluate_model()
#         )
#         return loss, number_of_evaluation_examples, {"accuracy": accuracy}


# def start_cluster_aggregator_as_learner() -> None:
#     max_retries = 10
#     retry_delay = 20
#     for attempt in range(max_retries):
#         try:
#             flwr.client.start_numpy_client(
#                 server_address=f"{get_context().aggregator_ip}:8080",
#                 client=ClusterAggregatorAsLearner(),
#             )
#             return
#         except Exception as e:
#             if attempt < max_retries:
#                 logger.exception(
#                     " ".join(
#                         (
#                             "Unable to connect to the root aggregator.",
#                             f"Retrying in '{retry_delay}' seconds."
#                             f"'{max_retries - attempt}' attempts remaining.",
#                         )
#                     )
#                 )
#                 time.sleep(retry_delay)
#             else:
#                 logger.error(
#                     f"Failed to connect to root aggregator after '{max_retries}' retries. '{e}'"
#                 )
#                 return
