# Note: Currently not needed, but just in case

# import os

# import pymongo
# from flops.process import FlOpsProcess
# from icecream import ic
# from utils.common import ROOT_FL_MANAGER_IP
# from utils.logging import logger

# ROOT_FL_MONGO_DB_PORT = os.environ.get("ROOT_FL_MONGO_DB_PORT")
# FLOPS_DB_NAME = "flops"
# FLOPS_PROCESSES_COLLECTION_NAME = "processes"


# def handle_database() -> None:
#     logger.debug("AAA")
#     client = pymongo.MongoClient(ROOT_FL_MANAGER_IP, int(ROOT_FL_MONGO_DB_PORT))
#     db = client[FLOPS_DB_NAME]
#     collection = db[FLOPS_PROCESSES_COLLECTION_NAME]

#     ic(client)
#     ic(db)
#     ic(collection)

#     logger.debug("BBB")

#     test_process = FlOpsProcess()

#     logger.debug("ZZZ")
