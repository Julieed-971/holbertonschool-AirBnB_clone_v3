#!/usr/bin/python3
"""

"""

import json
from api.v1.views import app_views
from flask import Response, jsonify


@app_views.route("/status", strict_slashes=False)
def return_status():
    """Returns app_views object status as a JSON file"""
    json_data = json.dumps({"status": "OK"}, indent=4)
    return Response(json_data + '\n', mimetype='application/json')
