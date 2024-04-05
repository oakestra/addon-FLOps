from api.consts import SYSTEM_MANAGER_URL
from api.custom_requests import CustomRequest, HttpMethods, RequestAuxiliaries, RequestCore
from flops.process import FlOpsProcess
from utils.exceptions import FLUIException
from utils.sla_generator import (
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
    generate_sla,
)
from utils.types import Sla


def generate_fl_ui_sla(flops_process: FlOpsProcess, url: str, port: str, ui_ip: str) -> Sla:
    return generate_sla(
        core=SlaCore(
            customerID=flops_process.customer_id,
            names=SlaNames(
                app_name=f"fl{flops_process.get_shortened_id()}",
                app_namespace="flui",
                service_name=f"fl{flops_process.get_shortened_id()}",
                service_namespace="flui",
            ),
            compute=SlaCompute(
                code="ghcr.io/malyuk-a/fl-ui:latest",
                cmd=f"python main.py {flops_process.flops_id} {url} {port}",
            ),
        ),
        details=SlaDetails(
            rr_ip=ui_ip,
            resources=SlaResources(memory=200, vcpus=1, storage=0),
        ),
    )


def send_fl_ui_creation_request(
    fl_ui_SLA: Sla,
    bearer_token: str,
    flops_process: FlOpsProcess,
) -> dict:
    return CustomRequest(
        RequestCore(
            http_method=HttpMethods.POST,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint="/api/application/",
            data=fl_ui_SLA,
            custom_headers={"Authorization": bearer_token},
        ),
        RequestAuxiliaries(
            what_should_happen=f"Create new FL UI service '{flops_process.flops_id}'",
            flops_process=flops_process,
            show_msg_on_success=True,
            exception=FLUIException,
        ),
    ).execute()
