from bson.objectid import ObjectId
from database.main import get_flops_db
from pydantic import BaseModel
from pymongo.collection import Collection


def get_collection(cls) -> Collection:
    return get_flops_db().get_collection(cls.__name__)


def add_to_db(object: BaseModel) -> ObjectId:
    return get_collection(object.__class__).insert_one(object.model_dump()).inserted_id


def replace_in_db(object: BaseModel, db_collection_object_id: ObjectId) -> None:
    get_collection(object.__class__).replace_one(
        {"_id": db_collection_object_id}, object.model_dump()
    )


def remove_from_db(cls, flops_project_id: str) -> None:
    get_collection(cls).delete_one({"flops_project_id": flops_project_id})


def retrieve_from_db(cls: BaseModel, flops_project_id: str) -> BaseModel:
    found_db_object = get_collection(cls).find_one({"flops_project_id": flops_project_id})
    found_db_object["gets_loaded_from_db"] = True
    return cls.model_validate(found_db_object)
