
import os
import json
from flask import escape
from threading import Thread
from datetime import datetime
from classes.Logger import Logger
from classes.MongoManager import MongoManager

logger = Logger().getLogger()


class Operations():
    def __init__(self):
        self.mongo_client = MongoManager().getClient()
        self.petrol_collec = MongoManager().getCollec()

    def get_all_information(self):
        try:
            result = json.dumps(list(self.petrol_collec.find({}, {'_id': 0})), ensure_ascii=False)
            self.mongo_client.close()

            return result

        except Exception:
            logger.exception()
            return

    def get_filter_distinct(self, filter):
        try:
            result = json.dumps(list(self.petrol_collec.find({}, {'_id': 0}).distinct(escape(filter))), ensure_ascii=False)
            self.mongo_client.close()

            return result

        except Exception:
            logger.exception()
            return

    def get_latest(self):
        try:
            query = "this._id.getTimestamp() >= ISODate('{}')".format(datetime.today().strftime('%Y-%m-%d'))
            result = json.dumps(list(self.petrol_collec.find({'$where': query}, {'_id': 0})), ensure_ascii=False)
            self.mongo_client.close()

            return result

        except Exception:
            logger.exception()
            return

    def update(self):
        try:
            os.system('. venv/bin/activate && python3 import.py')
        except Exception:
            logger.exception()