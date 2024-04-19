#!/usr/bin/python3
"""
View for State objects handling all default RESTFul API actions
"""

import json


from api.v1.views import app_views
from flask import abort, make_response, request
from models import storage
from models.state import State


def send_error():
    return abort(404, {"error": "Not found"})


def get_all():
    """"Returns list of all states"""
    all_states_list = []
    all_states = storage.all(State)
    for id in all_states:
        state = all_states[id]
        all_states_list.append(state.to_dict())
    return all_states_list


def get_by_id(state_id):
    """Retrieves a State object based on its id"""
    for state in get_all():
        if state_id == state["id"]:
            return make_response(state, 200)
    return send_error()


def delete_by_id(state_id):
    """Delete a state object based on its id"""
    state = storage.get(State, state_id)
    if state is None:
        return send_error()
    else:
        state.delete()
        storage.save()
        return make_response({}, 200)


def handle_request():
    """
        Handles GET request for all State objects
    """
    return make_response(get_all(), 200)


def handle_request_by_id(state_id: str):
    """
        Handles GET and DELETE requests
        for State objects
    """
    if (request.method == "PUT"):
        return update(state_id, request.get_json())
    elif (request.method == "GET"):
        return get_by_id(state_id)
    elif (request.method == "DELETE"):
        return delete_by_id(state_id)
    return send_error()


def create():
    """
        Creates a State object based on JSON request
    """
    try:
        state = State(**request.get_json(silent=True))
        if state.name is None:
            return make_response({"error": "Missing name"}, 400)
        state.save()
        return make_response(state.to_dict(), 201)
    except Exception:
        return abort(400, {"error": "Not a JSON"})


unauthorized_keys = {
    "id": True,
    "created_at": True,
    "updated_at": True
}


def update(state_id, data):
    """Update a state name by id"""
    try:
        states = storage.all(State)
        for state in states.values():
            if state.id == state_id:
                for key in data:
                    if (key not in unauthorized_keys):
                        setattr(state, key, data[key])

                state.save()
                return make_response(state.to_dict(), 200)
        return send_error()

    except Exception:
        return abort(400, {"error": "Not a JSON"})


@app_views.route(
    "/states",
    methods=['GET', 'DELETE', 'POST', 'PUT'],
    strict_slashes=False,
    defaults={'state_id': None}
)
@app_views.route(
    "/states/<state_id>",
    methods=['PUT', 'DELETE', 'GET']
)
def listen(state_id):
    """Retrieves list of all State objects"""
    if state_id is None:
        if (request.method == "POST"):
            return create()
        else:
            return handle_request()
    else:
        return handle_request_by_id(state_id)
