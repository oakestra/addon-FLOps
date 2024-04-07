import os

import pymongo
from utils.common import ROOT_FL_MANAGER_IP

ROOT_FL_MONGO_DB_PORT = os.environ.get("ROOT_FL_MONGO_DB_PORT")

_flops_db = None


class FLOpsDB:
    def __init__(self):
        self._client = pymongo.MongoClient(ROOT_FL_MANAGER_IP, int(ROOT_FL_MONGO_DB_PORT))
        self._db = self._client["flops"]
        global _flops_db
        _flops_db = self

    def get_collection(self, collection_name: str):
        return self._db[collection_name]


def get_flops_db() -> FLOpsDB:
    return _flops_db or FLOpsDB()
