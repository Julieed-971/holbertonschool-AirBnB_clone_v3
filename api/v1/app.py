#!/usr/bin/python3
"""
starts a Flask web application
"""

import json

from api.v1.views import app_views
from flask import Flask, Response
from models import storage
from werkzeug.exceptions import NotFound


my_app = Flask(__name__)
my_app.register_blueprint(app_views)


@my_app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@my_app.errorhandler(NotFound)
def handle_404_error(e):
    """
        Handles 404 errors and returns a
        JSON-formatted 404 status code response
    """
    data = json.dumps(
        {"error": "Not found"},
        indent=4
    )
    return Response(
        data + '\n',
        status=404,
        content_type="application/json"
    )


if __name__ == '__main__':
    my_app.run(host='0.0.0.0', port='5000', threaded=True)
