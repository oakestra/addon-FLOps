from flops.process import FlOpsProcess
from utils.common import FLOPS_USER_ACCOUNT
from utils.sla_generator import (
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
    generate_sla,
)
from utils.types import Sla

AGGREGATOR_APP_NAMESPACE = "flaggr"


def generate_aggregator_sla(
    flops_process: FlOpsProcess,
) -> Sla:

    aggregator_name = f"ag{flops_process.flops_id}"

    cmd = " ".join(
        (
            "python3",
            "main.py",
        )
    )

    return generate_sla(
        core=SlaCore(
            customerID=FLOPS_USER_ACCOUNT,
            names=SlaNames(
                app_name=aggregator_name,
                app_namespace=AGGREGATOR_APP_NAMESPACE,
                service_name=aggregator_name,
                service_namespace=AGGREGATOR_APP_NAMESPACE,
            ),
            compute=SlaCompute(
                # TODO put image into real OAK registry instead of private one
                code="ghcr.io/malyuk-a/fl-aggregator:latest",
                one_shot_service=True,
                cmd=cmd,
            ),
        ),
        details=SlaDetails(
            app_desc="fl_plugin application - FL aggregator",
            resources=SlaResources(
                memory=1000,
                vcpus=1,
                storage=1000,
            ),
        ),
    )
