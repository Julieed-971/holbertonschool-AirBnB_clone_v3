#!/usr/bin/python3
"""
View for City objects handling all default RESTFul API actions
"""

import json


from api.v1.views import app_views, states
from flask import jsonify, make_response, request, abort
from models import storage
from models.state import City, State


def send_error():
    return abort(404, {"error": "Not found"})


def get_cities_by_state_id(state_id):
    """
        Retrieves all cities by state_id
    """
    for state in storage.all(State).values():
        if state.id == state_id:
            all_cities = [city.to_dict() for city in state.cities]
            return make_response(all_cities, 200)
    return send_error()


def create_by_state_id(state_id, data: dict):
    """
        Create a city by state_id
    """
    print(state_id, data)
    try:
        # create city by state_id
        city = City(**data)
        if city.name is None:
            abort(400, {"error": "Missing name"})
        elif not storage.get(State, state_id):
            return send_error()
        city.state_id = state_id
        city.save()
        return make_response(city.to_dict(), 200)
    except (Exception):
        return make_response('Not a JSON', 400)


def get_cities_by_city_id(city_id):
    """
        Returns a city by city_id
    """
    for city in storage.all(City).values():
        if city.id == city_id:
            return make_response(city.to_dict(), 200)
    return send_error()


def delete_by_id(city_id):
    """
        Delete a city by city_id
    """
    city = storage.get(City, city_id)
    if city is None:
        return send_error()
    else:
        city.delete()
        storage.save()
        return jsonify({}), 200


unauthorized_keys = {
    "id": True,
    "state_id": True,
    "created_at": True,
    "updated_at": True
}


def update_city_by_id(city_id, data: dict):
    """
        Update a city by city_id
    """
    try:
        cities = storage.all(City)
        for city in cities.values():
            if city.id == city_id:
                for key in data:
                    if (key not in unauthorized_keys):
                        setattr(city, key, data[key])
                city.save()
                return make_response(city.to_dict(), 200)
        return send_error()

    except Exception:
        abort(400, {"error": "Not a JSON"})


@app_views.route(
    "/states/<state_id>/cities",
    methods=['GET', 'POST'],
    strict_slashes=False
)
def listen_states(state_id):
    """Retrieves list of all City object of a State"""
    if (request.method == "GET"):
        return get_cities_by_state_id(state_id)
    return create_by_state_id(state_id, request.get_json())


@app_views.route(
    "cities/<city_id>",
    methods=['GET', 'DELETE', 'PUT'],
    strict_slashes=False
)
def listen_cities(city_id):
    """Retrieve a city by id"""
    if (request.method == 'PUT'):
        return update_city_by_id(city_id, request.get_json())
    if (request.method == "DELETE"):
        return delete_by_id(request.get_json())
    return get_cities_by_city_id(city_id)
