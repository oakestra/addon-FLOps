import mqtt.main
from flops.image_builder_management.common import BUILDER_APP_NAMESPACE, MlRepo
from flops.image_registry.common import ROOT_FL_IMAGE_REGISTRY_URL
from flops.process import FlOpsProcess
from icecream import ic
from utils.common import FLOPS_USER_ACCOUNT
from utils.sla_generator import (
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
    generate_sla,
)
from utils.types import SLA


def generate_builder_sla(
    ml_repo: MlRepo,
    flops_process: FlOpsProcess,
) -> SLA:

    builder_name = f"bu{flops_process.flops_process_id}"

    cmd = " ".join(
        (
            "python3",
            "main.py",
            ml_repo.url,
            ROOT_FL_IMAGE_REGISTRY_URL,
            flops_process.flops_process_id,
            # TODO need to figure out a way to provide
            # non docker-compose member exclusive DNS name as IP.
            # mqtt.main.ROOT_MQTT_BROKER_URL,
            "192.168.178.44",
            mqtt.main.ROOT_FL_MQTT_BROKER_PORT,
            str(flops_process.ui_ip),
        )
    )

    resulting_sla = generate_sla(
        core=SlaCore(
            customerID=FLOPS_USER_ACCOUNT,
            names=SlaNames(
                app_name=builder_name,
                app_namespace=BUILDER_APP_NAMESPACE,
                service_name=builder_name,
                service_namespace=BUILDER_APP_NAMESPACE,
            ),
            compute=SlaCompute(
                code="ghcr.io/oakestra/plugins/flops/fl-client-env-builder:latest",
                one_shot_service=True,
                cmd=cmd,
            ),
        ),
        details=SlaDetails(
            app_desc="fl_plugin application for building FL client env images",
            resources=SlaResources(
                memory=2000,
                vcpus=1,
                storage=15000,
            ),
        ),
    )
    ic(f"Created builder SLA based on '{ml_repo.url}'", resulting_sla)
    return resulting_sla
