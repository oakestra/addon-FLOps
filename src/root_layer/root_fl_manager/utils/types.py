import enum


class CustomEnum(enum.Enum):
    def __str__(self) -> str:
        return self.value


SLA = dict
FL_SLA = SLA

ID = str
SERVICE_ID = ID
APPLICATION_ID = ID

DB_SERVICE_OBJECT = dict
