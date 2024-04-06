from flops.process import FlOpsProcess
from utils.sla_generator import (
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
    generate_sla,
)
from utils.types import SLA


def generate_fl_ui_sla(flops_process: FlOpsProcess, url: str, port: str, ui_ip: str) -> SLA:
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
                cmd=f"python main.py {flops_process.flops_process_id} {url} {port}",
            ),
        ),
        details=SlaDetails(
            rr_ip=ui_ip,
            resources=SlaResources(memory=200, vcpus=1, storage=0),
        ),
    )
