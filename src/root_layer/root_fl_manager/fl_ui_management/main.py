from http import HTTPStatus

import api.utils
from mqtt.main import ROOT_FL_MQTT_BROKER_PORT, ROOT_FL_MQTT_BROKER_URL
from utils.exceptions import FLUIServiceCreationException
from utils.identifier import FlOpsIdentifier
from utils.sla_generator import generate_sla
from utils.types import FL_SLA, SERVICE_ID


def create_fl_ui_service(
    new_fl_service_sla: FL_SLA,
    bearer_token: str,
    flops_identifier: FlOpsIdentifier,
) -> SERVICE_ID:

    url = ROOT_FL_MQTT_BROKER_URL
    port = ROOT_FL_MQTT_BROKER_PORT

    fl_ui_service_SLA = generate_sla(
        customerID=new_fl_service_sla["customerID"],
        app_name=f"fl{flops_identifier.flops_id}",
        app_namespace="flui",
        service_name=f"fl{flops_identifier.flops_id}",
        service_namespace="flui",
        code="ghcr.io/malyuk-a/fl-ui:latest",
        cmd=f"python main.py {flops_identifier.flops_id} {url} {port}",
        memory=200,
        storage=0,
        vcpus=1,
        rr_ip=flops_identifier.fl_ui_ip,
    )
    status, json_data = api.utils.handle_request(
        base_url=api.common.SYSTEM_MANAGER_URL,
        http_method=api.common.HttpMethod.POST,
        headers={"Authorization": bearer_token},
        data=fl_ui_service_SLA,
        api_endpoint="/api/application/",
        what_should_happen=f"Create new FL UI service '{flops_identifier.flops_id}'",
        show_msg_on_success=True,
    )
    if status != HTTPStatus.OK:
        raise FLUIServiceCreationException()

    return json_data[0]["microservices"][0]
