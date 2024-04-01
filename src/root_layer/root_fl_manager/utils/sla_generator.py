import ipaddress
import shlex
from typing import NamedTuple

from utils.types import ApplicationId, Sla


class SlaNames(NamedTuple):
    app_name: str = ""
    app_namespace: str = ""
    service_name: str = ""
    service_namespace: str = ""


class SlaCompute(NamedTuple):
    code: str
    one_shot_service: bool = False
    cmd: str = ""


class SlaCore(NamedTuple):
    names: SlaNames = SlaNames()
    compute: SlaCompute = None
    customerID: str = ""
    app_id: ApplicationId = ""


class SlaResources(NamedTuple):
    memory: int = 0
    vcpus: int = 0
    storage: int = 0


class SlaDetails(NamedTuple):
    resources: SlaResources = SlaResources()
    app_desc: str = ""
    rr_ip: ipaddress.IPv4Address = None


def generate_sla(
    core: SlaCore,
    details: SlaDetails,
) -> Sla:
    sla = {
        "sla_version": "v2.0",
        "customerID": core.customerID,
        "applications": [
            {
                "applicationID": core.app_id,
                "application_name": core.names.app_name,
                "application_namespace": core.names.app_namespace,
                "application_desc": details.app_desc,
                "microservices": [],
            }
        ],
    }
    if core.compute:
        sla["applications"][0]["microservices"].append(
            {
                "microserviceID": "",
                "microservice_name": core.names.service_name,
                "microservice_namespace": core.names.service_namespace,
                "virtualization": "container",
                "one_shot": core.compute.one_shot_service,
                "cmd": [] if (core.compute.cmd == "") else shlex.split(core.compute.cmd),
                "memory": details.resources.memory,
                "vcpus": details.resources.vcpus,
                "storage": details.resources.storage,
                "code": core.compute.code,
                **({"addresses": {"rr_ip": str(details.rr_ip)}} if details.rr_ip else {}),
            }
        )
    return sla
