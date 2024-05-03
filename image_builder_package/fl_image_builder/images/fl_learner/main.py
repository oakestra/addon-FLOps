import time
from typing import Any

import flwr
from flops_utils.logging import logger

# Note: This is part of the "to-be" injected client ML repo.
from model_manager import ModelManager
from utils.arg_parsing import parse_args


class Learner(flwr.client.NumPyClient):

    def __init__(self):
        self.model_manager = ModelManager()
        # Only for developing/testing
        self.model_manager.prepare_data()

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


def _start_fl_learner() -> None:
    aggregator_ip = parse_args()

    max_retries = 10
    retry_delay = 20

    # Note: The FL Learner image might be pulled and running quicker than the aggregator.
    # For these cases we want to wait for the aggregator to come online.
    # Compared to other solutions where the Learners are only deployed once the Aggregator is up,
    # this approach has the benefit of pulling/instantiating the learners concurrently/quicker.
    for attempt in range(max_retries):
        try:
            flwr.client.start_numpy_client(
                server_address=f"{aggregator_ip}:8080", client=Learner()
            )
            return
        except Exception as e:
            if attempt < max_retries:
                logger.warning(
                    " ".join(
                        (
                            "Unable to connect to aggregator.",
                            f"Retrying in '{retry_delay}' seconds."
                            f"'{max_retries - attempt}' attempts remaining.",
                        )
                    )
                )
                time.sleep(retry_delay)
            else:
                logger.error(
                    f"Failed to connect to aggregator after '{max_retries}' retries. '{e}'"
                )
                return


if __name__ == "__main__":
    _start_fl_learner()
