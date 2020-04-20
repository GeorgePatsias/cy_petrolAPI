import flask
from flask import jsonify
from threading import Thread

from classes.Logger import Logger
from classes.Operations import Operations
from classes.Auth import api_authentication
from classes.MongoManager import MongoManager

operation = Operations()
logger = Logger().getLogger()
mongo_client = MongoManager().getClient()
petrol_collec = MongoManager().getCollec()


app = flask.Blueprint('api_calls', __name__)


@app.route('/api/view/all', methods=['GET'])
@api_authentication
def all_information():
    try:
        return operation.get_all_information(), 200

    except Exception:
        logger.exception()
        return jsonify({'Status': 'Something went wrong'}), 500


@app.route('/api/view/<string:filter>', methods=['GET'])
@api_authentication
def filter_distinct(filter=None):
    try:
        return operation.get_filter_distinct(filter), 200

    except Exception:
        logger.exception()
        return jsonify({'Status': 'Something went wrong'}), 500


@app.route('/api/view/latest', methods=['GET'])
@api_authentication
def latest_information():
    try:
        return operation.get_latest(), 200

    except Exception:
        logger.exception()
        return jsonify({'Status': 'Something went wrong'}), 500


@app.route('/api/update', methods=['GET'])
@api_authentication
def scrape_new():
    try:
        Thread(target=operation.update).start()

        return jsonify({'Status': 'OK'}), 200

    except Exception:
        logger.exception()
        return jsonify({'Status': 'Something went wrong'}), 500
