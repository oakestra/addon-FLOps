from typing import Any

from flops_utils.types import AggregatorType
from pydantic import BaseModel, Field

# NOTE: The approach of using a global variable does not work here.
# So the context object gets injected into the methods as a parameter instead.
# Perhaps this is due to concurrent/background FLWR things that lack access to this variable.


class WinnerModel(BaseModel):
    # NOTE: IDs are strings because MLflow also uses strings for them.
    experiment_id: str
    run_id: str
    accuracy: float
    loss: float


class AggregatorContext(BaseModel):
    flops_project_id: str
    mqtt_ip: str
    project_observer_ip: str
    mlflow_tracking_server_url: str

    aggregator_type: AggregatorType = AggregatorType.CLASSIC_AGGREGATOR

    training_iterations: int = Field(
        default=1,
        description="""
            A training iteration is an umbrella term that can either mean
            a training round or a training cycle, depending on the current aggregator type.
            """,
    )
    min_available_clients: int = 1
    min_fit_clients: int = 1
    min_evaluate_clients: int = 1
    # For development purposes
    track_locally: bool = False  # Does not use the remote tracking server
    deactivate_notifications: bool = False  # Does not use MQTT

    root_aggregator_ip: str = ""

    winner_model: WinnerModel = Field(
        default=None,
        description="The best model after training.",
    )

    should_use_mlflow: bool = False

    def model_post_init(self, __context: Any) -> None:
        if self.aggregator_type != AggregatorType.CLUSTER_AGGREGATOR:
            self.should_use_mlflow = True
        return super().model_post_init(__context)
