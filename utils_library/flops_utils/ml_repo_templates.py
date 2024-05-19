from abc import ABC, abstractmethod
from typing import Any, Tuple


class LearnerDataManagerTemplate(ABC):

    @abstractmethod
    def get_data(self) -> Tuple[Any, Any]:
        """Gets the necessary data for training and evaluation.

        Examples:
        - self.training_data, self.testing_data
          which were set in the init like this: tf.keras.datasets.cifar10.load_data()
        """


class ModelManagerTemplate(ABC):

    @abstractmethod
    def prepare_data(self) -> None:
        """Gets the date from the DataManager and makes it available to the model.
        Make sure to now prepare the data in the ModelManager init function.
        This will avoid the aggregator from trying and fetch the data too.
        Data fetching is reserved for Learners.

        Heavily depends on the underlying model and ML library.

        Will be called by FLOps.

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
