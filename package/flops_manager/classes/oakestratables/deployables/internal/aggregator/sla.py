# import flops_manager.mqtt.main

# from flops.classes.abstract.base import FlOpsBaseClass
from flops_manager.utils.constants import FLOPS_USER_ACCOUNT
from flops_manager.utils.sla.components import (
    SlaComponentsWrapper,
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
)


# def prepare_aggregator_sla_components(aggregator: FlOpsBaseClass) -> SlaComponentsWrapper:
def prepare_aggregator_sla_components(aggregator) -> SlaComponentsWrapper:
    flops_project = aggregator.flops_project
    ui = aggregator.ui
    cmd = " ".join(
        (
            "python3",
            "main.py",
            # FLOPS_IMAGE_REGISTRY_URL,
            # flops_project.flops_project_id,
            # # TODO need to figure out a way to provide
            # # non docker-compose member exclusive DNS name as IP.
            # # mqtt.main.ROOT_MQTT_BROKER_URL,
            # "192.168.178.44",
            # mqtt.main.FLOPS_MQTT_BROKER_PORT,
            # ui.ip,
        )
    )

    return SlaComponentsWrapper(
        core=SlaCore(
            app_id=flops_project.flops_project_id,
            customerID=FLOPS_USER_ACCOUNT,
            names=SlaNames(
                app_name=flops_project.project_app_name,
                app_namespace=flops_project.namespace,
                service_name=f"ag{flops_project.get_shortened_id()}",
                service_namespace=aggregator.namespace,
            ),
            compute=SlaCompute(
                code="ghcr.io/malyuk-a/fl-aggregator:latest",
                one_shot_service=True,
                cmd=cmd,
            ),
        ),
        details=SlaDetails(
            resources=SlaResources(
                memory=100,
                vcpus=1,
                storage=0,
            ),
        ),
    )
