from typing import Any, Optional, Tuple

from aggregator_management import handle_aggregator
from flops_utils.ml_repo_files_proxy import get_model_manager
from flops_utils.ml_repo_templates import ModelManagerTemplate
from strategies.main import FLOpsFedAvg
from utils.aggregator_context import AggregatorContext


class ClusterAggregatorModelManager(ModelManagerTemplate):
    def __init__(self, aggregator_context: AggregatorContext):
        self.aggregator_context = aggregator_context
        # NOTE: This will return the model_manager of the real user-provided/configured ML repo.
        # i.e. The CAg Model Manager uses the ML Repo Model Manager.
        self.ml_repo_model_manager = get_model_manager()
        self.used_strategy: Optional[FLOpsFedAvg] = None

    def set_model_data(self) -> None:
        # NOTE: This empty method is necessary due to the abstract template parent class,
        # but the CAg does not have nor need any data itself.
        pass

    def get_model(self) -> Any:
        return self.ml_repo_model_manager.get_model()  # type: ignore

    def get_model_parameters(self) -> Any:
        return self.ml_repo_model_manager.get_model_parameters()  # type: ignore

    def set_model_parameters(self, parameters) -> None:
        self.ml_repo_model_manager.set_model_parameters(parameters)  # type: ignore

    def fit_model(self) -> int:
        # NOTE: This runs a CAg - Cluster-Learners FL training cycle.
        self.ml_repo_model_manager, self.used_strategy = handle_aggregator(
            aggregator_context=self.aggregator_context,
            model_manager=self.ml_repo_model_manager,
        )
        return self.used_strategy.current_cycles_number_of_training_examples

    def evaluate_model(self) -> Tuple[Any, Any, int]:
        # NOTE: The CAg cannot/should-not run a separate FL round/cycle just for evaluation.
        # The evaluation has already occurred during the fitting/training.
        current_cycles_losses = self.used_strategy.current_cycles_losses  # type: ignore
        loss = sum(current_cycles_losses) / len(current_cycles_losses)
        current_cycles_accuracies = self.used_strategy.current_cycles_accuracies  # type: ignore
        accuracy = sum(current_cycles_accuracies) / len(current_cycles_accuracies)
        return (
            loss,
            accuracy,
            self.used_strategy.current_cycles_number_of_evaluation_examples,  # type: ignore
        )
