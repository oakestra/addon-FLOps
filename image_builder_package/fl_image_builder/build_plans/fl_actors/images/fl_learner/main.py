import time
from typing import Any

import flwr
import grpc
import grpc._channel
from context import get_context
from flops_utils.logging import logger
from flops_utils.ml_repo_files_proxy import get_model_manager
from utils.arg_parsing import parse_args


class Learner(flwr.client.NumPyClient):

    def __init__(self):
        logger.debug("Start Learner Init")
        self.model_manager = get_model_manager()
        self.model_manager.set_model_data()
        logger.debug("Finished Learner Init")

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
        loss, accuracy, number_of_evaluation_examples = self.model_manager.evaluate_model()
        return loss, number_of_evaluation_examples, {"accuracy": accuracy}


def _start_fl_learner() -> None:
    retry_delay = 20

    # NOTE:
    # The FL Learner image might be pulled and running quicker than the aggregator.
    # For these cases we want to wait for the aggregator to come online.
    # Compared to other solutions where the Learners are only deployed once the Aggregator is up,
    # this approach has the benefit of pulling/instantiating the learners concurrently/quicker.
    #
    # The learner is a continuous service.
    # I.e. once a training cycle ends the learners awaits a potential successor cycle.
    # This is necessary for hierarchical FL.
    # Classic FL will only run a single cycle and undeploy this service via the FLOps Manager.
    #
    # We tried using the new Flower NEXT Server and Client Apps (since v1.8.0).
    # They seem very promising but currently there seems to be only support for static,
    # stateless CLI usage, which does not fit our use case - so we stick with the legacy way.
    while True:
        try:
            flwr.client.start_numpy_client(
                server_address=f"{get_context().aggregator_ip}:8080",
                client=Learner(),
            )
        except grpc._channel._MultiThreadedRendezvous as e:
            logger.warning("GRPC Channel Exception Detected")
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                logger.warning(f"grpc.StatusCode.UNAVAILABLE - retrying in '{retry_delay}' s")
                # NOTE: This exact exception occurs if the Learner cannot reach the Aggregator.
                # The main reason why this can be is if the Learner service/image starts
                # (e.g. gets pulled) faster than the Aggregator service/image.
                time.sleep(retry_delay)
                continue
            logger.error("Unexpected GRPC Channel Exception Detected")
            raise e
        except Exception as e:
            logger.error("Unexpected Exception Detected")
            raise e


if __name__ == "__main__":
    parse_args()
    _start_fl_learner()
