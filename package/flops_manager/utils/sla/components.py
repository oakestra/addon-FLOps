import ipaddress
from typing import NamedTuple

from utils.types import ApplicationId


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


class SlaComponentsWrapper(NamedTuple):
    core: SlaCore
    details: SlaDetails
