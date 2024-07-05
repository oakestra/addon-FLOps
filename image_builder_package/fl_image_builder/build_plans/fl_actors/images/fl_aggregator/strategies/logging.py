import flwr as fl
import mlflow
from flops_utils.ml_model_flavor_proxy import get_ml_model_flavor

DEFAULT_SYSTEM_METRICS_LOGGING_INTERVAL = 10  # seconds

current_system_metrics_logging_interval = DEFAULT_SYSTEM_METRICS_LOGGING_INTERVAL


def _update_system_metrics_logging_interval(new_interval: int) -> None:
    global current_system_metrics_logging_interval
    current_system_metrics_logging_interval = new_interval
    mlflow.set_system_metrics_sampling_interval(new_interval)


def handle_system_metrics_logging() -> None:
    """Ensures that even fast runs have system metrics by adjusting the logging interval.

    MLflow logs system metrics every 10 seconds by default.
    If a run takes less time no system metrics will be logged for it.

    https://mlflow.org/docs/latest/system-metrics/index.html#customizing-logging-frequency
    """
    run_start = mlflow.last_active_run().info.start_time  # type: ignore
    run_end = mlflow.last_active_run().info.end_time  # type: ignore
    run_duration = (run_end - run_start) / 1000
    if (
        run_duration < DEFAULT_SYSTEM_METRICS_LOGGING_INTERVAL
        and current_system_metrics_logging_interval == DEFAULT_SYSTEM_METRICS_LOGGING_INTERVAL
    ):
        _update_system_metrics_logging_interval(run_duration / 2)
        return

    if (
        run_duration > DEFAULT_SYSTEM_METRICS_LOGGING_INTERVAL
        and current_system_metrics_logging_interval < DEFAULT_SYSTEM_METRICS_LOGGING_INTERVAL
    ):
        _update_system_metrics_logging_interval(DEFAULT_SYSTEM_METRICS_LOGGING_INTERVAL)
        return


def init_logging() -> None:
    get_ml_model_flavor().autolog()
    mlflow.enable_system_metrics_logging()


def log_project_params(strategy: fl.server.strategy.Strategy) -> None:
    interesting_params = [
        "min_available_clients",
        "min_evaluate_clients",
        "min_fit_clients",
        "fraction_evaluate",
        "fraction_fit",
    ]
    mlflow.log_params(
        dict(filter(lambda pair: pair[0] in interesting_params, list(vars(strategy).items())))
    )
