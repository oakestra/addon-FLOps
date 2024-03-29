import ipaddress
import shlex

from utils.types import APPLICATION_ID, SLA


def generate_sla(
    code: str,
    customerID: str = "",
    app_id: APPLICATION_ID = "",
    app_name: str = "",
    app_namespace: str = "",
    app_desc: str = "",
    service_name: str = "",
    service_namespace: str = "",
    one_shot_service: bool = False,
    cmd: str = "",
    memory: int = 0,
    vcpus: int = 0,
    storage: int = 0,
    rr_ip: ipaddress.IPv4Address = None,
) -> SLA:
    return {
        "sla_version": "v2.0",
        "customerID": customerID,
        "applications": [
            {
                "applicationID": app_id,
                "application_name": app_name,
                "application_namespace": app_namespace,
                "application_desc": app_desc,
                "microservices": [
                    {
                        "microserviceID": "",
                        "microservice_name": service_name,
                        "microservice_namespace": service_namespace,
                        "virtualization": "container",
                        "one_shot": one_shot_service,
                        "cmd": [] if (cmd == "") else shlex.split(cmd),
                        "memory": memory,
                        "vcpus": vcpus,
                        "storage": storage,
                        "code": code,
                        **({"addresses": {"rr_ip": str(rr_ip)}} if rr_ip else {}),
                    }
                ],
            }
        ],
    }
