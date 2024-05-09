from pydantic import BaseModel

# Note: The approach of using a global variable does not work here.
# Perhaps this is due to concurrent/background FLWR things that lack access to this variable.


class AggregatorContext(BaseModel):
    flops_project_id: str
    mqtt_ip: str
    project_observer_ip: str
    mlflow_tracking_server_url: str

    training_rounds: int = 3
    min_available_clients: int = 1
    min_fit_clients: int = 1
    min_evaluate_clients: int = 1
