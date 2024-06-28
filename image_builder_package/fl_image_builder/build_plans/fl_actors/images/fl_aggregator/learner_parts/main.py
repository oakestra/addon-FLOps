import time
from typing import Any

import flwr
from flops_utils.logging import logger
from learner_parts.model_manager import ClusterAggregatorModelManager
from utils.aggregator_context import AggregatorContext


# NOTE/TODO: This is almost identical to the Learner Class in the fl_actors/images/fl_learner.
# Maybe move this into the flops_utils lib and share the code
# The only change necessary is to add an optional input param
# - (special) ModelManager object instance (necessary for the CAg)
#   if not specified - use the normal get_model_manager() function call.
# Plus the optional aggregator_context as input param too.
class ClusterAggregatorAsLearner(flwr.client.NumPyClient):
    def __init__(self, aggregator_context: AggregatorContext):
        logger.info("INIT ClusterAggregatorAsLearner")
        self.aggregator_context = aggregator_context
        self.model_manager = ClusterAggregatorModelManager(self.aggregator_context)
        self.model_manager.set_model_data()

    def get_parameters(self, config=None) -> Any:
        return self.model_manager.get_model_parameters()

    def set_parameters(self, parameters) -> None:
        self.model_manager.set_model_parameters(parameters)

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        number_of_training_examples = self.model_manager.fit_model()
        return self.get_parameters(), number_of_training_examples, {}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        loss, accuracy, number_of_evaluation_examples = (
            self.model_manager.evaluate_model()
        )
        return loss, number_of_evaluation_examples, {"accuracy": accuracy}


def start_cluster_aggregator_as_learner(aggregator_context: AggregatorContext) -> None:
    logger.info("START start_cluster_aggregator_as_learner")
    max_retries = 10
    retry_delay = 20
    for attempt in range(max_retries):
        try:
            flwr.client.start_numpy_client(
                server_address=f"{aggregator_context.root_aggregator_ip}:8080",
                client=ClusterAggregatorAsLearner(aggregator_context),
            )
            return
        except Exception as e:
            if attempt < max_retries:
                logger.exception(
                    " ".join(
                        (
                            "Unable to connect to the root aggregator.",
                            f"Retrying in '{retry_delay}' seconds."
                            f"'{max_retries - attempt}' attempts remaining.",
                        )
                    )
                )
                time.sleep(retry_delay)
            else:
                logger.error(
                    f"Failed to connect to root aggregator after '{max_retries}' retries. '{e}'"
                )
                return
