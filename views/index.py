import flask
from flask import render_template, jsonify

from classes.Logger import Logger
from classes.Auth import api_authentication
from classes.MongoManager import MongoManager

logger = Logger().getLogger()
mongo_client = MongoManager().getClient()
petrol_collec = MongoManager().getCollec()

app = flask.Blueprint('index', __name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# @app.route('/user_management', methods=['GET'])
# @login_required
# @requires_roles('superadmin')
# def user_management():
#     csrf_token = gen_csrf_token()
#     return render_template('user_management.html', csrf_token=csrf_token)