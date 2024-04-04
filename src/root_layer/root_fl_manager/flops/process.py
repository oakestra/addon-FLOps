import ipaddress
import uuid


class FlOpsProcess:
    """Represents all necessary FL and ML/DevOps components to power one entire FL user request.

    This includes:
    - FL_UI service
    - Image Builder service
    - FL aggregator
    - FL clients
    - connected MLOps

    The FLOpsProcess ID is interwined in all mentioned components for easy grouping/mapping/linking.
    It is enough to  forward this ID to external components.
    Based on the ID alone the original FlOpsProcess object can be reconstructed,
    thus avoiding the need for storing it persistently e.g. via a dedicated DB.
    """

    def _generate_ip(self, offset: int = 0) -> ipaddress.IPv4Address:
        unique_int = int(self.id, 16) % 65536
        third_octet = (unique_int + offset) // 256
        forth_octet = (unique_int + offset) % 256
        return ipaddress.IPv4Address(f"10.30.{third_octet}.{forth_octet}")

    def __init__(self, id: str = None):
        self.id = id or str(uuid.uuid4())[:6]
        self.fl_ui_ip = self._generate_ip()
        self.fl_aggregator_ip = self._generate_ip(offset=1)
