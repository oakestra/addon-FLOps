import mqtt.main
from image_builder_management.common import BUILDER_APP_NAMESPACE
from image_builder_management.repo_management import MlRepo
from image_registry.common import ROOT_FL_IMAGE_REGISTRY_URL
from utils.common import FLOPS_USER_ACCOUNT
from utils.types import SLA


def generate_builder_sla(
    ml_repo: MlRepo,
    service_id: str,
) -> SLA:
    builder_app_name = f"{str(ml_repo.github_repo.id)[0]}{ml_repo.latest_commit_hash}"
    return {
        "sla_version": "v2.0",
        "customerID": FLOPS_USER_ACCOUNT,
        "applications": [
            {
                "applicationID": "",
                "application_name": builder_app_name,
                "application_namespace": BUILDER_APP_NAMESPACE,
                "application_desc": "fl_plugin application for building FL client env images",
                "microservices": [
                    {
                        "microserviceID": "",
                        "microservice_name": "builder",
                        "microservice_namespace": BUILDER_APP_NAMESPACE,
                        "virtualization": "container",
                        "one_shot": True,
                        "cmd": [
                            "python3",
                            "main.py",
                            ml_repo.url,
                            ROOT_FL_IMAGE_REGISTRY_URL,
                            service_id,
                            # TODO need to figure out a way to provide
                            # non docker-compose member exclusive DNS name as IP.
                            # mqtt.main.ROOT_MQTT_BROKER_URL,
                            "192.178.168.44",
                            mqtt.main.ROOT_MQTT_BROKER_PORT,
                            builder_app_name,
                        ],
                        "memory": 2000,
                        "vcpus": 1,
                        "storage": 15000,
                        # TODO CHANGE THIS once the proper image is no longer private !
                        "code": "ghcr.io/malyuk-a/fl-client-env-builder:latest",
                        # "code": "ghcr.io/oakestra/plugins/flops/fl-client-env-builder:latest",
                    }
                ],
            }
        ],
    }
