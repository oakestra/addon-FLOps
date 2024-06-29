from typing import Any, Tuple

from aggregator_management import handle_aggregator
from flops_utils.logging import logger
from flops_utils.ml_repo_files_proxy import get_model_manager
from flops_utils.ml_repo_templates import ModelManagerTemplate
from utils.aggregator_context import AggregatorContext


class ClusterAggregatorModelManager(ModelManagerTemplate):
    def __init__(self, aggregator_context: AggregatorContext):
        logger.info("INIT ClusterAggregatorModelManager")
        self.aggregator_context = aggregator_context
        # NOTE: This will return the model_manager of the real user-provided/configured ML repo.
        # i.e. The CAg Model Manager uses the ML Repo Model Manager.
        self.ml_repo_model_manager = get_model_manager()
        logger.info("FIN ClusterAggregatorModelManager")

    def set_model_data(self) -> None:
        # NOTE/TODO: Only for testing:
        # Afterwards need to set to "pass"
        # Still need this due to abstract template parent class,
        # but the CAg does not have any data itself.
        self.ml_repo_model_manager.set_model_data()

    def get_model(self) -> Any:
        logger.info("get_model")
        return self.ml_repo_model_manager.get_model()

    def get_model_parameters(self) -> Any:
        logger.info("get_model_parameters")
        return self.ml_repo_model_manager.get_model_parameters()

    def set_model_parameters(self, parameters) -> None:
        logger.info("set_model_parameters")
        self.ml_repo_model_manager.set_model_parameters(parameters)

    def fit_model(self) -> int:
        logger.info("fit_model")

        # TODO Need to run n FL training rounds
        updated_model_manager, used_strategy = handle_aggregator(
            aggregator_context=self.aggregator_context,
            model_manager=self.ml_repo_model_manager,
        )
        self.ml_repo_model_manager = updated_model_manager
        return used_strategy.total_number_of_training_examples

        # logger.info("START _set_init_params")
        # init_params_context = self.aggregator_context.model_copy()
        # init_params_context.training_iterations = 1
        # init_params_context.deactivate_notifications = True
        # handle_aggregator(aggregator_context=init_params_context)
        # logger.info("FIN _set_init_params")

        # # Ignore convergence failure due to low local epochs
        # with warnings.catch_warnings():
        #     warnings.simplefilter("ignore")
        #     self.model.fit(self.x_train, self.y_train)
        # return len(self.x_train)

        # return self.ml_repo_model_manager.fit_model()

    def evaluate_model(self) -> Tuple[Any, Any, int]:
        logger.info("evaluate_model")

        # For evaluation the underlying user ML repo code will be used directly.
        return self.ml_repo_model_manager.evaluate_model()

        # loss = log_loss(self.y_test, self.model.predict_proba(self.x_test))
        # accuracy = self.model.score(self.x_test, self.y_test)
        # # return loss, len(self.x_test), {"accuracy": accuracy}
        # return loss, accuracy, len(self.x_test)
