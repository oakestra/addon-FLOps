import ipaddress
from typing import ClassVar, List, NamedTuple

from flops_manager.utils.types import ApplicationId
from pydantic import BaseModel, Field

FLOPS_LEARNER_ADDON_TYPE = "FLOps-learner"


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


class SlaConstraint(BaseModel):
    type: ClassVar[str]

    # NOTE: The .model_dump_json() or other methods do not include ClassVars.
    def to_json_dict(self) -> dict:
        return {"type": self.type}


class LatencyConstraint(SlaConstraint):
    type = "latency"
    # TODO
    pass


class GeoConstraint(SlaConstraint):
    type = "geo"
    # TODO
    pass


class AddonConstraint(SlaConstraint):
    type = "addons"
    needs: List[str] = Field(
        default_factory=list,
        examples=["addon_1", "addon_2"],
        description="Allows placement only on worker nodes where requested addons are installed.",
    )

    def to_json_dict(self) -> dict:
        object_representation = super().to_json_dict()
        object_representation["needs"] = self.needs
        return object_representation


class SlaDetails(NamedTuple):
    resources: SlaResources = SlaResources()
    app_desc: str = ""
    rr_ip: ipaddress.IPv4Address = None
    port: str = None
    privileged: bool = False
    constraints: List[SlaConstraint] = []


class SlaComponentsWrapper(NamedTuple):
    core: SlaCore
    details: SlaDetails = SlaDetails()
    core: SlaCore
    details: SlaDetails = SlaDetails()
