import json
from datetime import datetime
from flask import Flask, jsonify, request, escape

from classes.Auth import Auth
from classes.Logger import Logger
from classes.MongoManager import MongoManager

Auth = Auth()
logger = Logger().getLogger()
petrol_collec = MongoManager().getCollec()

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = app.config['FLASK_SECRET_KEY']


@app.route('/api/view/all', methods=['GET'])
def all_information():
    try:
        if not Auth.isValid(request.headers.get('Authorization', None)):
            return jsonify({'Status': 'Unauthorized'}), 401

        db_results = list(petrol_collec.find({}, {'_id': 0}))

        return json.dumps(db_results, ensure_ascii=False), 200

    except Exception as e:
        logger.exception(e)
        return jsonify({'Status': 'Something went wrong'}), 500


@app.route('/api/view/<string:distinct>', methods=['GET'])
def petrol_types(distinct=None):
    try:
        if not Auth.isValid(request.headers.get('Authorization', None)):
            return jsonify({'Status': 'Unauthorized'}), 401

        db_results = list(petrol_collec.find({}, {'_id': 0}).distinct(escape(distinct)))

        return json.dumps(db_results, ensure_ascii=False), 200

    except Exception as e:
        logger.exception(e)
        return jsonify({'Status': 'Something went wrong'}), 500


@app.route('/api/view/latest', methods=['GET'])
def latest_information():
    try:
        if not Auth.isValid(request.headers.get('Authorization', None)):
            return jsonify({'Status': 'Unauthorized'}), 401

        query = "this._id.getTimestamp() >= ISODate('{}')".format(datetime.today().strftime('%Y-%m-%d'))
        db_results = list(petrol_collec.find({'$where': query}, {'_id': 0}))

        return json.dumps(db_results, ensure_ascii=False), 200

    except Exception as e:
        logger.exception(e)
        return jsonify({'Status': 'Something went wrong'}), 500


if __name__ == '__main__':
    logger.info('~~~ PetrolAPI Server Started ~~~')

    app.run(host='0.0.0.0', port=1337, debug=True, threaded=True)
