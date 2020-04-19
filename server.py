import json
from datetime import datetime
from threading import Thread
from flask import Flask, jsonify, request, escape

from classes.Logger import Logger
from classes.Operations import Operations
from classes.Auth import api_authentication
from classes.MongoManager import MongoManager

operation = Operations()
logger = Logger().getLogger()
mongo_client = MongoManager().getClient()
petrol_collec = MongoManager().getCollec()

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = app.config['FLASK_SECRET_KEY']

@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Type'] = 'application/json'
    return response


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
        Thread(target=operation.update()).start()
        # operation.update()

        return jsonify({'Status': 'OK'}), 200

    except Exception:
        logger.exception()
        return jsonify({'Status': 'Something went wrong'}), 500


if __name__ == '__main__':
    logger.info('~~~ PetrolAPI Server Started ~~~')

    app.run(host='0.0.0.0', port=1337, debug=True)
