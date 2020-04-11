
import json
import datetime
from flask import escape
from classes.MongoManager import MongoManager


class Operations():
    def __init__(self):
        self.mongo_client = MongoManager().getClient()
        self.petrol_collec = MongoManager().getCollec()

    def get_all_information(self):
        result = json.dumps(list(self.petrol_collec.find({}, {'_id': 0})), ensure_ascii=False)
        self.mongo_client.close()

        return result

    def get_filter_distinct(self, filter):
        result = json.dumps(list(petrol_collec.find({}, {'_id': 0}).distinct(escape(filter))), ensure_ascii=False)
        self.mongo_client.close()

        return result

    def get_latest(self):
        query = "this._id.getTimestamp() >= ISODate('{}')".format(datetime.today().strftime('%Y-%m-%d'))
        result = json.dumps(list(petrol_collec.find({'$where': query}, {'_id': 0})), ensure_ascii=False)
        self.mongo_client.close()

        return result
