from api.consts import SYSTEM_MANAGER_URL
from api.custom_requests import CustomRequest, HttpMethod, RequestAuxiliaries, RequestCore
from mqtt.main import ROOT_FL_MQTT_BROKER_PORT, ROOT_FL_MQTT_BROKER_URL
from utils.exceptions import FLUIException
from utils.identifier import FlOpsIdentifier
from utils.sla_generator import (
    SlaCompute,
    SlaCore,
    SlaDetails,
    SlaNames,
    SlaResources,
    generate_sla,
)
from utils.types import FlSla, ServiceId


def create_fl_ui_service(
    new_fl_service_sla: FlSla,
    bearer_token: str,
    flops_identifier: FlOpsIdentifier,
) -> ServiceId:

    url = ROOT_FL_MQTT_BROKER_URL
    port = ROOT_FL_MQTT_BROKER_PORT

    from icecream import ic

    fl_ui_service_SLA = generate_sla(
        core=SlaCore(
            customerID=new_fl_service_sla["customerID"],
            names=SlaNames(
                app_name=f"fl{flops_identifier.flops_id}",
                app_namespace="flui",
                service_name=f"fl{flops_identifier.flops_id}",
                service_namespace="flui",
            ),
            compute=SlaCompute(
                code="ghcr.io/malyuk-a/fl-ui:latest",
                cmd=f"python main.py {flops_identifier.flops_id} {url} {port}",
            ),
        ),
        details=SlaDetails(
            rr_ip=flops_identifier.fl_ui_ip,
            resources=SlaResources(memory=200, vcpus=1, storage=0),
        ),
    )

    ic("1", fl_ui_service_SLA)

    new_fl_ui_app = CustomRequest(
        RequestCore(
            http_method=HttpMethod.POST,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint="/api/application/",
            data=fl_ui_service_SLA,
            custom_headers={"Authorization": bearer_token},
        ),
        RequestAuxiliaries(
            what_should_happen=f"Create new FL UI service '{flops_identifier.flops_id}'",
            flops_identifier=flops_identifier,
            show_msg_on_success=True,
            exception=FLUIException,
        ),
    )

    ic("2", new_fl_ui_app)

    return new_fl_ui_app[0]["microservices"][0]


def deploy_fl_ui_service(fl_ui_service_id: ServiceId) -> None:
    CustomRequest(
        RequestCore(
            http_method=HttpMethod.POST,
            base_url=SYSTEM_MANAGER_URL,
            api_endpoint=f"/api/service/{fl_ui_service_id}/instance",
        ),
        RequestAuxiliaries(
            what_should_happen=f"Deploy FL UI service '{fl_ui_service_id}'",
            exception=FLUIException,
            show_msg_on_success=True,
        ),
    )
