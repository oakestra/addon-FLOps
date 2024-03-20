import mqtt.main
from image_builder_management.common import BUILDER_APP_NAMESPACE, MlRepo
from image_registry.common import ROOT_FL_IMAGE_REGISTRY_URL
from utils.common import FLOPS_USER_ACCOUNT
from utils.sla_generator import generate_sla
from utils.types import SERVICE_ID, SLA


def generate_builder_sla(
    ml_repo: MlRepo,
    original_ml_service_id: SERVICE_ID,
) -> SLA:

    builder_app_name = f"{str(ml_repo.github_repo.id)[0]}{ml_repo.latest_commit_hash}"

    cmd = " ".join(
        (
            "python3",
            "main.py",
            ml_repo.url,
            ROOT_FL_IMAGE_REGISTRY_URL,
            original_ml_service_id,
            # TODO need to figure out a way to provide
            # non docker-compose member exclusive DNS name as IP.
            # mqtt.main.ROOT_MQTT_BROKER_URL,
            "192.178.168.44",
            mqtt.main.ROOT_MQTT_BROKER_PORT,
            builder_app_name,
        )
    )

    return generate_sla(
        code="ghcr.io/oakestra/plugins/flops/fl-client-env-builder:latest",
        customerID=FLOPS_USER_ACCOUNT,
        app_name=builder_app_name,
        app_namespace=BUILDER_APP_NAMESPACE,
        app_desc="fl_plugin application for building FL client env images",
        service_name="builder",
        service_namespace=BUILDER_APP_NAMESPACE,
        one_shot_service=True,
        cmd=cmd,
        memory=2000,
        vcpus=1,
        storage=15000,
    )
