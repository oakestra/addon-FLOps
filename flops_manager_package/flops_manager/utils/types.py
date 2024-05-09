import enum


class CustomEnum(enum.Enum):
    def __str__(self) -> str:
        return self.value


SLA = dict
AppSLA = SLA

Application = dict
Service = dict

Id = str
ServiceId = Id
ApplicationId = Id
