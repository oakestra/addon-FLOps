import api.custom_requests as custom_requests
import flops.fl_ui_management.notification as ui_notifier
import utils.classes.exceptions as custom_exceptions
from api.consts import SYSTEM_MANAGER_URL
from api.custom_http import HttpMethods
from flops.aggregator_management.utils import generate_aggregator_sla
from flops.process import FlOpsProcess
from utils.logging import logger
from utils.types import ServiceId


def create_fl_aggregator(
    flops_process: FlOpsProcess,
    verbose: bool = False,
):
    aggregator_sla = generate_aggregator_sla(flops_process)
    aggregator_name = aggregator_sla["applications"][0]["application_name"]
    logger.debug(f"Created aggregator SLA: {aggregator_sla}")

    # Note: The called endpoint returns all apps of the user not just the newest inserted one.
    response = custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            http_method=HttpMethods.POST,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint="/api/application",
            data=aggregator_sla,
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen=f"Create new aggregator '{flops_process.flops_process_id}'",
            exception=custom_exceptions.ImageBuilderException,
            show_msg_on_success=True,
        ),
    ).execute()

    if verbose:
        ui_notifier.notify_ui(
            "FL Aggregator created",
            flops_process,
        )

    new_aggregator_app = next(
        (app for app in response if app["application_name"] == aggregator_name), None
    )
    if new_aggregator_app is None:
        raise custom_exceptions.ImageBuilderException(
            "Could not find new aggregator app after creating it", flops_process
        )

    return new_aggregator_app["microservices"][0]


def deploy_fl_aggregator_service(
    aggregator_service_id: ServiceId,
    flops_process: FlOpsProcess,
    verbose: bool = False,
) -> None:
    custom_requests.CustomRequest(
        core=custom_requests.RequestCore(
            http_method=HttpMethods.POST,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/service/{aggregator_service_id}/instance",
        ),
        aux=custom_requests.RequestAuxiliaries(
            what_should_happen=f"Deploy aggregator, id '{aggregator_service_id}'",
            exception=custom_exceptions.FlAggregatorException,
            show_msg_on_success=True,
        ),
    ).execute()
    if verbose:
        ui_notifier.notify_ui(
            "New Aggregator application deployed & started",
            flops_process,
        )


def handle_aggregator(flops_process: FlOpsProcess) -> None:
    fl_aggregator_id = create_fl_aggregator(flops_process)
    deploy_fl_aggregator_service(fl_aggregator_id, flops_process)
