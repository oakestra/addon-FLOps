import mqtt.main
from flops.classes.ml_repo import MlRepo
from flops.classes.process import FlOpsProcess
from flops.classes.ui import FLUserInterface
from flops.image_registry.common import ROOT_FL_IMAGE_REGISTRY_URL
from utils.common import FLOPS_USER_ACCOUNT
from utils.sla.components import (
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
    generate_sla,
)
from utils.types import SLA

BUILDER_APP_NAMESPACE = "flbuild"


def generate_builder_sla(
    ml_repo: MlRepo,
    flops_process: FlOpsProcess,
    fl_ui: FLUserInterface,
) -> SLA:

    builder_name = f"bu{flops_process.get_shortened_id()}"

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
            fl_ui.ip,
        )
    )

    return generate_sla(
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
