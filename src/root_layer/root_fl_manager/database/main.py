import os

import pymongo
from utils.common import ROOT_FL_MANAGER_IP
from utils.types import CustomEnum

ROOT_FL_MONGO_DB_PORT = os.environ.get("ROOT_FL_MONGO_DB_PORT")

_flops_db = None


class DbCollections(CustomEnum):
    PROCESSES = "processes"
    ML_REPOS = "ml_repos"
    USER_INTERFACES = "user_interfaces"


class FLOpsDB:
    def __init__(self):
        self._client = pymongo.MongoClient(ROOT_FL_MANAGER_IP, int(ROOT_FL_MONGO_DB_PORT))
        self._db = self._client["flops"]
        self._collections_dict = {
            collection_enum: self._db[str(collection_enum)] for collection_enum in DbCollections
        }
        global _flops_db
        _flops_db = self

    def get_collection(self, collection_enum: DbCollections):
        return self._collections_dict[collection_enum]


def get_flops_db() -> FLOpsDB:
    return _flops_db or FLOpsDB()
