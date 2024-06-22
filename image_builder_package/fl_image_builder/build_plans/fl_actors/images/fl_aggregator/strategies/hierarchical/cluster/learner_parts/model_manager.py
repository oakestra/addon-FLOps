import warnings
from typing import Any, Tuple

import mlflow
import mlflow.sklearn
import numpy as np
from data_manager import DataManager
from flops_utils.ml_repo_files_proxy import get_model_manager
from flops_utils.ml_repo_templates import ModelManagerTemplate
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss


class ClusterAggregatorModelManager(ModelManagerTemplate):
    def __init__(self):
        # NOTE: This will return the model_manager of the real user-provided/configured ML repo.
        self.model_manager = get_model_manager()
        self.model = self.model_manager.get_model()

        self._set_init_params()

    def _set_init_params(self) -> None:
        """Sets initial parameters as zeros Required since model params are uninitialized
        until model.fit is called.

        But the server (root aggregator) asks for initial parameters
        from clients (cluster aggregator) at launch.

        To get such initial parameters the CAg performs a minimal (1 training round long)
        yet real training with its learners.
        """

    def set_model_data(self) -> None:
        (self.x_train, self.x_test), (self.y_train, self.y_test) = (
            DataManager().get_data()
        )

    def get_model(self) -> Any:
        return self.model

    def get_model_parameters(self) -> Any:
        if self.model.fit_intercept:
            params = [
                self.model.coef_,
                self.model.intercept_,
            ]
        else:
            params = [
                self.model.coef_,
            ]
        return params

    def set_model_parameters(self, parameters) -> None:
        self.model.coef_ = parameters[0]
        if self.model.fit_intercept:
            self.model.intercept_ = parameters[1]

    def fit_model(self) -> int:
        # Ignore convergence failure due to low local epochs
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.model.fit(self.x_train, self.y_train)
        return len(self.x_train)

    def evaluate_model(self) -> Tuple[Any, Any, int]:
        loss = log_loss(self.y_test, self.model.predict_proba(self.x_test))
        accuracy = self.model.score(self.x_test, self.y_test)
        # return loss, len(self.x_test), {"accuracy": accuracy}
        return loss, accuracy, len(self.x_test)
