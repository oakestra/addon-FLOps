# from flops.classes.abstract.base import FlOpsBaseClass
from flops_manager.image_registry.common import FLOPS_IMAGE_REGISTRY_URL
from flops_manager.mqtt.main import FLOPS_MQTT_BROKER_PORT
from flops_manager.utils.constants import FLOPS_USER_ACCOUNT
from flops_manager.utils.sla.components import (
    SlaComponentsWrapper,
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
)


# def prepare_builder_sla_components(builder: FlOpsBaseClass) -> SlaComponentsWrapper:
def prepare_builder_sla_components(builder) -> SlaComponentsWrapper:
    flops_project = builder.flops_project
    ml_repo = builder.ml_repo
    ui = builder.ui
    cmd = " ".join(
        (
            "python3",
            "main.py",
            ml_repo.url,
            FLOPS_IMAGE_REGISTRY_URL,
            flops_project.flops_project_id,
            # TODO need to figure out a way to provide
            # non docker-compose member exclusive DNS name as IP.
            # mqtt.main.ROOT_MQTT_BROKER_URL,
            "192.168.178.44",
            FLOPS_MQTT_BROKER_PORT,
            ui.ip,
        )
    )

    return SlaComponentsWrapper(
        core=SlaCore(
            app_id=flops_project.flops_project_id,
            customerID=FLOPS_USER_ACCOUNT,
            names=SlaNames(
                app_name=flops_project.project_app_name,
                app_namespace=flops_project.namespace,
                service_name=f"bu{flops_project.get_shortened_id()}",
                service_namespace=builder.namespace,
            ),
            compute=SlaCompute(
                code="ghcr.io/oakestra/plugins/flops/fl-client-env-builder:latest",
                one_shot_service=True,
                cmd=cmd,
            ),
        ),
        details=SlaDetails(
            resources=SlaResources(
                memory=2000,
                vcpus=1,
                storage=15000,
            ),
        ),
    )
