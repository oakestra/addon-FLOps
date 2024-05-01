import enum


class CustomEnum(enum.Enum):
    def __str__(self) -> str:
        return self.value


SLA = dict
AppSLA = SLA

Application = dict

Id = str
ServiceId = Id
ApplicationId = Id
