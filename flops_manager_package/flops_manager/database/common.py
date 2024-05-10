from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from bson.objectid import ObjectId
from database.main import get_flops_db
from pydantic import BaseModel
from pymongo.collection import Collection

if TYPE_CHECKING:
    from flops_manager.classes.base import FlOpsOakestraBaseClass


def get_collection(cls) -> Collection:
    return get_flops_db().get_collection(cls.__name__)


def add_to_db(object: BaseModel) -> ObjectId:
    return get_collection(object.__class__).insert_one(object.model_dump()).inserted_id


def replace_in_db(object: BaseModel, db_collection_object_id: ObjectId) -> None:
    get_collection(object.__class__).replace_one(
        {"_id": db_collection_object_id}, object.model_dump()
    )


def retrieve_from_db_by_app_id(cls: BaseModel, app_id: str) -> BaseModel:
    return _load_object_from_retrieved_db_result(
        cls, get_collection(cls).find_one({"app_id": app_id})
    )


def retrieve_from_db_by_user_id(cls, user_id: str) -> Optional[dict]:
    return _load_object_from_retrieved_db_result(
        cls, get_collection(cls).find_one({"user_id": user_id})
    )


def retrieve_from_db_by_project_id(cls, flops_project_id: str) -> Optional[dict]:
    return _load_object_from_retrieved_db_result(
        cls, get_collection(cls).find_one({"flops_project_id": flops_project_id})
    )


def remove_from_db_by_project_id(cls, flops_project_id: str) -> None:
    get_collection(cls).delete_one({"flops_project_id": flops_project_id})


def _load_object_from_retrieved_db_result(
    cls: FlOpsOakestraBaseClass,
    found_db_object: dict,
) -> Optional[FlOpsOakestraBaseClass]:
    if not found_db_object:
        return None

    found_db_object["gets_loaded_from_db"] = True
    return cls.model_validate(found_db_object)
