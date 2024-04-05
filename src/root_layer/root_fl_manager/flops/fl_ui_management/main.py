from dataclasses import dataclass, field

from api.consts import SYSTEM_MANAGER_URL
from api.custom_requests import CustomRequest, HttpMethods, RequestAuxiliaries, RequestCore
from database.main import DbCollections, get_flops_db
from flops.fl_ui_management.utils import generate_fl_ui_sla, send_fl_ui_creation_request
from flops.process import FlOpsProcess
from flops.utils import generate_ip
from mqtt.main import ROOT_FL_MQTT_BROKER_PORT, ROOT_FL_MQTT_BROKER_URL
from utils.exceptions import FLUIException
from utils.types import FlOpsBaseClass, ServiceId


@dataclass
class FLUserInterface(FlOpsBaseClass):
    flops_process_id: str = field(init=False)
    ip: str = field(init=False, default="")
    fl_ui_id: str = field(init=False, default="")

    def __init__(self, flops_process: FlOpsProcess, auth_header: str):
        self.flops_process_id = flops_process.flops_id
        self.ip = generate_ip(flops_process.flops_id, self)
        self.fl_ui_id = self._create(flops_process, auth_header)
        self._deploy()
        self._add_to_db()

    def _create(
        self,
        flops_process: FlOpsProcess,
        bearer_token: str,
    ) -> ServiceId:
        fl_ui_SLA = generate_fl_ui_sla(
            flops_process=flops_process,
            port=ROOT_FL_MQTT_BROKER_PORT,
            url=ROOT_FL_MQTT_BROKER_URL,
            ui_ip=self.ip,
        )
        new_fl_ui_app = send_fl_ui_creation_request(
            fl_ui_SLA=fl_ui_SLA,
            bearer_token=bearer_token,
            flops_process=flops_process,
        )
        return new_fl_ui_app[0]["microservices"][0]

    def _deploy(self) -> None:
        CustomRequest(
            RequestCore(
                http_method=HttpMethods.POST,
                base_url=SYSTEM_MANAGER_URL,
                api_endpoint=f"/api/service/{self.fl_ui_id}/instance",
            ),
            RequestAuxiliaries(
                what_should_happen=f"Deploy FL UI service '{self.fl_ui_id}'",
                exception=FLUIException,
                show_msg_on_success=True,
            ),
        ).execute()

    def _add_to_db(self) -> None:
        db_collection = get_flops_db().get_collection(DbCollections.USER_INTERFACES)
        db_collection.insert_one(self.to_dict())
