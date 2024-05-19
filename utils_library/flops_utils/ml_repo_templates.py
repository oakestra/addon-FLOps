from abc import ABC, abstractmethod
from typing import Any, Tuple


class DataManagerTemplate(ABC):

    @abstractmethod
    def _prepare_data(self) -> Any:
        """Calls the load_ml_data function and does data preprocessing, etc. (optional)
        The Learner does not yet have the data from the worker node.
        To get this data please use the 'load_ml_data' function which can be imported like this:
        ```
        from flops_utils.flops_learner_files_wrapper import load_ml_data
        ```
        Once the data has been fetched, custom data preprocessing and augmentations can be applied.
        """

    @abstractmethod
    def get_data(self) -> Tuple[Any, Any]:
        """Get the necessary data for training and evaluation.
        This data has to be already prepared/preprocessed.

        This method is intended to be called by the ModelManager.

        Examples:
        - self.training_data, self.testing_data
        """


class ModelManagerTemplate(ABC):

    @abstractmethod
    def set_model_data(self) -> None:
        """Gets the data from the DataManager and makes it available to the model.
        Do not include this method call in the ModelManager init function.
        The aggregator also needs the model but does not have access to the data.

        This function will be called by the FLOps Learner only.

        Heavily depends on the underlying model and ML library.

        Examples: ()
        - self.trainloader, self.testloader = DataManager().get_data()
        - (self.x_train, self.y_train), (self.x_test, self.y_test) = (
            DataManager().get_data())
        """
        pass

    @abstractmethod
    def get_model(self) -> Any:
        """Gets the managed model.

        Examples:
        - self.model
        - tf.keras.applications.MobileNetV2(
            (32, 32, 3), classes=10, weights=None
        )"""
        pass

    @abstractmethod
    def get_model_parameters(self) -> Any:
        """Gets the model parameters.

        Examples:
        - self.model.get_weights()
        - [val.cpu().numpy() for _, val in self.model.state_dict().items()]
        """
        pass

    @abstractmethod
    def set_model_parameters(self, parameters) -> None:
        """Set the model parameters.

        Examples:
        - self.model.set_weights(parameters)
        - params_dict = zip(self.model.state_dict().keys(), parameters)
          state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
          self.model.load_state_dict(state_dict, strict=True)
        """
        pass

    @abstractmethod
    def fit_model(self) -> int:
        """Fits the model and returns the number of training samples.

        Examples of return values:
        - len(self.x_train)
        - len(self.trainloader.dataset)
        """
        pass

    @abstractmethod
    def evaluate_model(self) -> Tuple[Any, Any, int]:
        """Evaluates the model.

        Returns:
        - loss
        - accuracy
        - number of test/evaluation samples

        Examples of return values:
        - loss, accuracy, len(self.testloader.dataset)
        - loss, accuracy, len(self.x_test)
        """
        pass
