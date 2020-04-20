import os
from flask_cors import CORS
from flask_compress import Compress
from flask import Flask, send_from_directory


from classes.Logger import Logger

import views.api_calls
import views.index


logger = Logger().getLogger()

app = Flask(__name__)
CORS(app)
Compress(app)

app.config.from_pyfile('config.py')
app.secret_key = app.config['FLASK_SECRET_KEY']


app.register_blueprint(views.api_calls.app)
app.register_blueprint(views.index.app)


@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Type'] = 'application/json'
    response.headers['Expires'] = '-1'
    response.headers['Pragma'] = 'no-cache'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img/'), 'favicon.ico')


if __name__ == '__main__':
    logger.info('~~~ PetrolAPI Server Started ~~~')

    app.run(host='0.0.0.0', port=1337, debug=True, threaded=True)
