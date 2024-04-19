#!/usr/bin/python3
"""
    View for Users objects handling all default RESTFul API actions
"""


from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


# 04aa8357-59ec-44b3-b0db-5a5e8ceb5f58

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json(silent=True):
        abort(400, 'Missing email')
    if 'password' not in request.get_json(silent=True):
        abort(400, 'Missing password')
    user = User(**request.get_json(silent=True))
    user.save()
    return make_response(user.to_dict(), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in request.get_json(silent=True).items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return make_response(user.to_dict(), 200)
