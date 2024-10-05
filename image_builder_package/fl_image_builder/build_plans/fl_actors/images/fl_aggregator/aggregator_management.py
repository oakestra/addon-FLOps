import sys
from typing import Optional, Tuple

import flwr as fl
import mlflow
from flops_utils.logging import logger
from flops_utils.ml_repo_files_proxy import get_model_manager
from flops_utils.mqtt_topics import SupportedTopic
from flops_utils.notifications import notify_project_observer
from notification_management import (
    builder_notify_flops_manager,
    notify_about_failure_and_terminate,
    notify_about_successful_completion,
)
from strategies.main import FLOpsFedAvg
from utils.aggregator_context import AggregatorContext

FL_START_INFO_TEXT = """
Start Aggregator activities - Start Federated Learning:
Visit the page below to observe your (active) FLOps Project.
(Note: There you can observe the progress in real time.)
"""


def start_fl_server(aggregator_context: AggregatorContext, strategy, rounds):
    if not aggregator_context.deactivate_notifications:
        notify_project_observer(
            project_observer_ip=aggregator_context.project_observer_ip,
            msg=f"{FL_START_INFO_TEXT}\n '{aggregator_context.mlflow_tracking_server_url}'",
        )
        builder_notify_flops_manager(
            aggregator_context=aggregator_context,
            topic=SupportedTopic.AGGREGATOR_STARTED,
        )
    fl.server.start_server(
        server_address="0.0.0.0:8080",
        config=fl.server.ServerConfig(num_rounds=rounds),
        strategy=strategy,
    )
    if not aggregator_context.deactivate_notifications:
        notify_about_successful_completion(aggregator_context=aggregator_context)


def handle_aggregator(
    aggregator_context: AggregatorContext,
    model_manager: Optional[object] = None,
) -> Tuple[object, FLOpsFedAvg]:  # type: ignore
    """Handles the aggregator and runs all training rounds.

    If no model_manager (MM) instance/object has been provided as input,
    then a fresh new MM instance gets created just for this training cycle.

    If a MM is provided it will get used instead and returned afterwards.
    NOTE: this MM will be properly changed, e.g. its weights/model updated/trained.

    Returns an updated/trained MM and the Flower Strategy object that was used for training.

    NOTE: The strategy accumulates interesting/necessary information
    like the total number of training examples that were used.
    """

    try:
        model_manager = model_manager or get_model_manager()
        if not aggregator_context.track_locally and aggregator_context.should_use_mlflow:
            mlflow.set_tracking_uri(aggregator_context.mlflow_tracking_server_url)
        if aggregator_context.should_use_mlflow:
            # NOTE: A MLflow experiment consists of multiple runs.
            # For FLOps: experiment = project, run = Flower FL training + evaluation round.
            mlflow_experiment = mlflow.set_experiment(
                experiment_name=f"FLOps Project {aggregator_context.flops_project_id}"
            )
        strategy_instance = FLOpsFedAvg(
            aggregator_context=aggregator_context,
            model_manager=model_manager,
            mlflow_experiment_id=(
                mlflow_experiment.experiment_id if aggregator_context.should_use_mlflow else None
            ),
            # NOTE: The Flower Strategy lacks the notion of the number of expected training rounds.
            requested_total_number_of_training_rounds=aggregator_context.training_iterations,
            min_available_clients=aggregator_context.min_available_clients,
            min_fit_clients=aggregator_context.min_fit_clients,
            min_evaluate_clients=aggregator_context.min_evaluate_clients,
            # NOTE: Instead of waiting for a random Learner to provide the init params.
            # We let the Aggregator set the init params.
            #
            # Paper - 2022 - Nguyen et al.
            # "Where to Begin?
            # On the Impact of Pre-Training and Initialization in Federated Learning"
            # This paper proves that setting init params can give a massive boost/benefit.
            # (We are not doing anything fancy here yet - but this can be easily enhanced.)
            #
            # This also enables us to chain together multiple training cycles,
            # thus, enabling us to properly evolve a Hierarchical FL model,
            # because otherwise the Learners would always start from scratch.
            #
            # NOTE: Initial params only work if they are converted into the Flower Parameters Type.
            # (IMO this is poorly checked and documented from Flower's side.
            # The code still runs but behaves very strangely.
            # i.e. all Learner responses fail but the Aggregator continues
            # to fast-forward through his training-rounds.)
            # More info: https://discuss.flower.ai/t/how-do-i-start-from-a-pre-trained-model/73/2
            # TODO: Add a check in the builder to verify that the user provided code
            # (the get_params() method) can be properly transformed into Flower Parameters.
            # I.e. verify that the user provided code fits our FLOps requirements
            # (structural, methods, etc.)
            initial_parameters=fl.common.ndarrays_to_parameters(
                model_manager.get_model_parameters()  # type: ignore
            ),
        )
        start_fl_server(
            aggregator_context=aggregator_context,
            strategy=strategy_instance,
            rounds=aggregator_context.training_iterations,
        )
        return model_manager, strategy_instance

    except Exception as e:
        if aggregator_context.deactivate_notifications:
            logger.exception("Aggregation failed with exception.")
            sys.exit(1)

        notify_about_failure_and_terminate(
            aggregator_context=aggregator_context,
            error_msg=f"Aggregator failed: '{e}'",
        )
