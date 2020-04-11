from pymongo import MongoClient
from config import MONGO_DB, PETROL_COLLECTION, MONGO_CONNECTION


class MongoManager():
    def __init__(self):
        self.client = MongoClient(MONGO_CONNECTION, connect=False)
        self.db = self.client[MONGO_DB]
        self.petrol_collec = self.db[PETROL_COLLECTION]

    def getClient(self):
        return self.client
        
    def getCollec(self):
        return self.petrol_collec
