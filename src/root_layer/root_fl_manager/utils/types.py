import enum
from http import HTTPStatus
from typing import Tuple


class CustomEnum(enum.Enum):
    def __str__(self) -> str:
        return self.value


Sla = dict
FlSla = Sla

Id = str
ServiceId = Id
ApplicationId = Id

ExternalApiResponse = Tuple[dict, HTTPStatus]
