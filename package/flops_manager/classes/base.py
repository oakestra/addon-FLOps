from abc import ABC

from bson.objectid import ObjectId
from database.main import get_flops_db
from pydantic import BaseModel, Field
from pymongo.collection import Collection


class FlOpsBaseClass(BaseModel, ABC):
    flops_project_id: str

    gets_loaded_from_db: bool = Field(False, init=False, exclude=True, repr=False)

    @classmethod
    def get_collection(cls) -> Collection:
        return get_flops_db().get_collection(cls.__name__)

    def _add_to_db(self) -> ObjectId:
        return self.__class__.get_collection().insert_one(self.model_dump()).inserted_id

    def _replace_in_db(self, db_collection_object_id: ObjectId) -> None:
        self.__class__.get_collection().replace_one(
            {"_id": db_collection_object_id}, self.model_dump()
        )

    @classmethod
    def retrieve_from_db(cls, flops_project_id: str) -> "FlOpsBaseClass":
        found_db_object = cls.get_collection().find_one({"flops_project_id": flops_project_id})
        found_db_object["gets_loaded_from_db"] = True
        return cls.model_validate(found_db_object)
