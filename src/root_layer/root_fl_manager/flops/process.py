from dataclasses import dataclass

from database.main import DbCollections
from utils.classes.base import FlOpsBaseClass


@dataclass
class FlOpsProcess(FlOpsBaseClass):
    """Links all necessary FL and ML/DevOps components to power one entire FL user request."""

    customer_id: str
    verbose: bool = False

    def __post_init__(self):
        self.flops_process_id = ""  # Used to avoid breaking DB interactions.
        self.db_collection_type = DbCollections.PROCESSES
        flops_db_id = self._add_to_db()
        self.flops_process_id = str(flops_db_id)
        self._replace_in_db(flops_db_id)

    def get_shortened_id(self) -> str:
        return self.flops_process_id[:6]
