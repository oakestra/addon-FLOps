import enum


class CustomEnum(enum.Enum):
    def __str__(self) -> str:
        return self.value


class FLOpsImageType(CustomEnum):
    LEARNER = "learner"
    AGGREGATOR = "aggregator"


SLA = dict
AppSLA = SLA

Application = dict

Id = str
ServiceId = Id
ApplicationId = Id
