from config import API_KEY
from functools import wraps
from classes.Logger import Logger
from flask import request, make_response
logger = Logger().getLogger()


def api_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_key = request.headers.get('Authorization', None)

        if not auth_key or auth_key != API_KEY:
            logger.info('Invalid API key: {}'.format(auth_key))
            return make_response({"Status": "Unauthorized"}, 401)

        return f(*args, **kwargs)
    return decorated_function
