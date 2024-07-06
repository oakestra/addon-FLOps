import pymongo
from flops_manager.utils.env_vars import FLOPS_DB_PORT, FLOPS_MANAGER_IP

_flops_db = None


class FLOpsDB:
    def __init__(self):
        self._client = pymongo.MongoClient(FLOPS_MANAGER_IP, int(FLOPS_DB_PORT))
        self._db = self._client["flops"]
        global _flops_db
        _flops_db = self

    def get_collection(self, collection_name: str):
        return self._db[collection_name]

    def drop_all_collections(self):
        for coll_name in self._client.list_database_names():
            if coll_name == "flops":  # Ensure we're not trying to drop the database itself
                for collection_name in self._client[coll_name].list_collection_names():
                    self._client[coll_name].drop_collection(collection_name)


def get_flops_db() -> FLOpsDB:
    return _flops_db or FLOpsDB()


def reset_db() -> None:
    assert _flops_db is not None
    _flops_db.drop_all_collections()
