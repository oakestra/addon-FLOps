from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field

import database.main as db
from bson.objectid import ObjectId
from pymongo.collection import Collection


@dataclass
class FlOpsBaseClass(ABC):
    # Note: These vars need to be set in each child class.
    flops_process_id: str = field(init=False)

    def __init__(self, flops_process_id: str):
        self.flops_process_id = flops_process_id

    def to_dict(self):
        return asdict(self)

    @abstractmethod
    @classmethod
    def from_dict(cls, data) -> "FlOpsBaseClass":
        return cls(**data)

    @classmethod
    def get_collection(cls) -> Collection:
        return db.get_flops_db().get_collection(cls.__name__)

    def _add_to_db(self) -> ObjectId:
        return self.__class__.get_collection().insert_one(self.to_dict()).inserted_id

    def _replace_in_db(self, db_collection_object_id: ObjectId) -> None:
        self.__class__.get_collection().replace_one(
            {"_id": db_collection_object_id}, self.to_dict()
        )

    @classmethod
    def retrieve_from_db(cls, flops_process_id: str) -> "FlOpsBaseClass":
        return cls.from_dict(cls.get_collection().find_one({"flops_process_id": flops_process_id}))
