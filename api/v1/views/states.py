#!/usr/bin/python3
"""
View for State objects handling all default RESTFul API actions
"""

import json


from api.v1.views import app_views
from flask import jsonify, request, Response
from models import storage
from models.state import State
from typing import List


def send_error():
    return jsonify({"error": "Not found"}), 404


def get_all() -> List[dict]:
    """"Returns list of all states"""
    all_states_list = []
    all_states = storage.all(State)
    for id in all_states:
        state = all_states[id]
        all_states_list.append(state.to_dict())
    return all_states_list


def get_by_id(state_id: str):
    """Retrieves a State object based on its id"""
    for state in get_all():
        if state_id == state["id"]:
            return jsonify(state), 200
    return send_error()


def delete_by_id(state_id: str):
    """Delete a state object based on its id"""
    state: State = storage.get(State, state_id)
    if state is None:
        return send_error()
    else:
        state.delete()
        storage.save()
        return jsonify({}), 200


def handle_request():
    """
        Handles GET request for all State objects
    """
    return jsonify(get_all()), 200


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


def create(data: dict):
    """
        Creates a State object based on JSON request
    """
    try:
        state = State(**data)
        if state.name is None:
            return Response(
                '{"error": "Missing name"}\n',
                status=400,
                mimetype='application/json'
            )
        state.save()
        return jsonify(state.to_dict()), 201
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400


unauthorized_keys = {
    "id": True,
    "created_at": True,
    "updated_at": True
}


def update(state_id, data: dict):
    """Update a state name by id"""
    try:
        states = storage.all(State)
        for state in states.values():
            if state.id == state_id:
                for key in data:
                    if (key not in unauthorized_keys):
                        setattr(state, key, data[key])

                state.save()
                return jsonify(state.to_dict()), 200
        return send_error()

    except Exception:
        return Response(
            '{"error": "Not a JSON"}\n',
            status=400,
            mimetype='application/json'
        )


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
            return create(request.get_json())
        else:
            return handle_request()
    else:
        return handle_request_by_id(state_id)
