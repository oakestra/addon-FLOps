_ui_context = None


class UIContext:
    def __init__(
        self,
        flops_id: str,
        mqtt_ip: str,
        mqtt_port: str,
    ):
        self.flops_id = flops_id
        self.mqtt_ip = mqtt_ip
        self.mqtt_port = mqtt_port

        global _ui_context
        _ui_context = self


def get_ui_context() -> UIContext:
    return _ui_context  # type: ignore
