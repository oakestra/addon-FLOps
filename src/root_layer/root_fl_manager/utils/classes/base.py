from abc import ABC

import database.main as db
from bson.objectid import ObjectId
from pydantic import BaseModel
from pymongo.collection import Collection


class FlOpsBaseClass(BaseModel, ABC):
    flops_process_id: str

    @classmethod
    def get_collection(cls) -> Collection:
        return db.get_flops_db().get_collection(cls.__name__)

    def _add_to_db(self) -> ObjectId:
        return self.__class__.get_collection().insert_one(self.model_dump()).inserted_id

    def _replace_in_db(self, db_collection_object_id: ObjectId) -> None:
        self.__class__.get_collection().replace_one(
            {"_id": db_collection_object_id}, self.model_dump()
        )

    @classmethod
    def retrieve_from_db(cls, flops_process_id: str) -> "FlOpsBaseClass":
        return cls.model_validate(
            cls.get_collection().find_one({"flops_process_id": flops_process_id})
        )
