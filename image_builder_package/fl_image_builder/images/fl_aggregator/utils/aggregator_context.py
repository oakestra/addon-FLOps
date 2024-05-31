from pydantic import BaseModel, Field

# Note: The approach of using a global variable does not work here.
# So the context object gets injected into the methods as a parameter instead.
# Perhaps this is due to concurrent/background FLWR things that lack access to this variable.


class WinnerModel(BaseModel):
    # Note: IDs are strings because MLflow also uses strings for them.
    experiment_id: str
    run_id: str
    accuracy: float
    loss: float


class AggregatorContext(BaseModel):
    flops_project_id: str
    mqtt_ip: str
    project_observer_ip: str
    mlflow_tracking_server_url: str

    training_rounds: int = 3
    min_available_clients: int = 1
    min_fit_clients: int = 1
    min_evaluate_clients: int = 1
    # For development purposes
    track_locally: bool = False  # Does not use the remote tracking server
    deactivate_notifications: bool = False  # Does not use MQTT

    winner_model: WinnerModel = Field(
        default=None,
        description="The best model after training.",
    )
