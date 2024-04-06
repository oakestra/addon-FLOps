from abc import ABC
from dataclasses import asdict, dataclass, field
from typing import ClassVar

from bson.objectid import ObjectId
from database.main import DbCollections, get_flops_db


@dataclass
class FlOpsBaseClass(ABC):
    # Note: These vars need to be set in each child class.
    db_collection_type: ClassVar[DbCollections]
    flops_process_id: str = field(init=False)

    def __init__(self, db_collection_type: DbCollections, flops_process_id: str):
        self.db_collection_type = db_collection_type
        self.flops_process_id = flops_process_id

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def _add_to_db(self):  # TODO
        return (
            get_flops_db()
            .get_collection(self.db_collection_type)
            .insert_one(self.to_dict())
            .inserted_id
        )

    def _replace_in_db(
        self,
        db_collection_object_id,
    ) -> None:  # TODO
        get_flops_db().get_collection(self.db_collection_type).replace_one(
            {"_id": ObjectId(db_collection_object_id)}, self.to_dict()
        )
