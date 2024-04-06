from dataclasses import dataclass, field

from bson.objectid import ObjectId
from database.main import DbCollections, get_flops_db
from utils.types import FlOpsBaseClass


@dataclass
class FlOpsProcess(FlOpsBaseClass):
    """Links all necessary FL and ML/DevOps components to power one entire FL user request."""

    customer_id: str
    verbose: bool = False

    flops_id: str = field(init=False, default="")

    def __post_init__(self):
        db_collection = get_flops_db().get_collection(DbCollections.PROCESSES)
        flops_db_id = db_collection.insert_one(self.to_dict()).inserted_id
        self.flops_id = str(flops_db_id)
        db_collection.replace_one({"_id": ObjectId(flops_db_id)}, self.to_dict())

    def get_shortened_id(self) -> str:
        return self.flops_id[:6]
