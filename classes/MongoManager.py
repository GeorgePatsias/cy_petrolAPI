from pymongo import MongoClient


class MongoManager():
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/', connect=False)
        self.db = self.client['my_information3']
        self.petrol_collec = self.db['all_petrol']

    def getCollec(self):
        return self.petrol_collec