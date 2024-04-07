import mqtt.main as main_mqtt
from flops.fl_ui_management.utils import generate_fl_ui_sla
from flops.process import FlOpsProcess
from flops.utils import generate_ip
from utils.classes.complex import FlOpsDeployableClass
from utils.types import AppSLA


class FLUserInterface(FlOpsDeployableClass):
    ip: str = ""

    def model_post_init(self, _):
        if not self.ip:
            self.ip = generate_ip(self.flops_process_id, self)

    def _create_sla(self, flops_process: FlOpsProcess) -> AppSLA:
        return generate_fl_ui_sla(
            flops_process=flops_process,
            port=main_mqtt.ROOT_FL_MQTT_BROKER_PORT,
            url=main_mqtt.ROOT_FL_MQTT_BROKER_URL,
            ui_ip=self.ip,
        )
