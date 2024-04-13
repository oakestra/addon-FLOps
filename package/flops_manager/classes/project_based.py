from abc import ABC

from flops_manager.classes.base import FlOpsBaseClass


class FlOpsProjectBasedClass(FlOpsBaseClass, ABC):
    flops_project_id: str

    @classmethod
    def retrieve_from_db(cls, flops_project_id: str) -> "FlOpsProjectBasedClass":
        found_db_object = cls.get_collection().find_one({"flops_project_id": flops_project_id})
        found_db_object["gets_loaded_from_db"] = True
        return cls.model_validate(found_db_object)
