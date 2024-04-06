from dataclasses import dataclass, field

from database.main import DbCollections
from flops.fl_ui_management.utils import generate_fl_ui_sla
from flops.process import FlOpsProcess
from flops.utils import generate_ip
from mqtt.main import ROOT_FL_MQTT_BROKER_PORT, ROOT_FL_MQTT_BROKER_URL
from utils.classes.complex import FlOpsDeployableClass


@dataclass
class FLUserInterface(FlOpsDeployableClass):
    ip: str = field(init=False, default="")

    def __init__(self, flops_process: FlOpsProcess, auth_header: str):
        super().__init__(DbCollections.USER_INTERFACES, flops_process.flops_process_id)
        self.ip = generate_ip(flops_process.flops_process_id, self)
        fl_ui_SLA = generate_fl_ui_sla(
            flops_process=flops_process,
            port=ROOT_FL_MQTT_BROKER_PORT,
            url=ROOT_FL_MQTT_BROKER_URL,
            ui_ip=self.ip,
        )
        self._create(flops_process, fl_ui_SLA, auth_header)
        self.__post_init__()
