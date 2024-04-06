import enum
from dataclasses import asdict, dataclass


class CustomEnum(enum.Enum):
    def __str__(self) -> str:
        return self.value


@dataclass
class FlOpsBaseClass:
    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


Sla = dict
FlOpsProcessSla = Sla

Id = str
ServiceId = Id
ApplicationId = Id
