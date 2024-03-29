import ipaddress
import uuid


class FlOpsIdentifier:
    def __init__(self):
        self.flops_id = str(uuid.uuid4())[:6]
        unique_int = int(self.flops_id, 16) % 65536
        self.fl_ui_ip = ipaddress.IPv4Address(f"10.30.{unique_int // 256}.{unique_int % 256}")
