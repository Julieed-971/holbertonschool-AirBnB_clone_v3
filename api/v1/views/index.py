#!/usr/bin/python3
"""

"""

import json

from api.v1.views import app_views
from flask import Response
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.state import State
from models.city import City
from models.user import User
from models import storage


@app_views.route("/status", strict_slashes=False)
def return_status():
    """Returns app_views object status as a JSON file"""
    json_data = json.dumps({"status": "OK"})
    return Response(json_data + '\n', mimetype='application/json')


@app_views.route("/stats", strict_slashes=False)
def return_stats():
    """Returns app_views object status as a JSON file"""
    data = {}
    data['amenities'] = storage.count(Amenity)
    data['cities'] = storage.count(City)
    data['places'] = storage.count(Place)
    data['reviews'] = storage.count(Review)
    data['states'] = storage.count(State)
    data['users'] = storage.count(User)
    return Response(
        json.dumps(data) + '\n',
        mimetype='application/json'
    )
