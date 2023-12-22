#!/usr/bin/env python3
"""The blueprint for all CRUD operation for user."""
from models.user import User
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from api.v1.views import get_match, delete_match, update_match, register_new, validate_id, validate_user

parent_cls = User


@app_views.route(
    "/users",
    methods=["GET"],
    strict_slashes=False,
    defaults={"user_id": None},
)
@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Get all user or get a particular user by id."""
    
    if user_id:
      # validate id
        if validate_id(user_id) is False:
            return jsonify({"error" :"id is not of type uuid"}), 404
        return get_match(parent_cls, user_id)
    user = [users.to_dict() for users in storage.all(parent_cls).values()]
    return jsonify(user)


@app_views.route(
    "/users/<user_id>",
    methods=["DELETE"],
    strict_slashes=False
)
def delete_user(user_id):
    """Delete a user by id."""
    return delete_match(parent_cls, user_id)


@app_views.route(
    "/users",
    methods=["POST"],
    strict_slashes=False,
)
def register_user():
    """Register a new user via a POST request."""
    if not request.json:
        return jsonify({"error" :"Not a valid JSON"}), 400
    if "name" not in request.json:
        return jsonify({"error" :"Missing name"}), 400
    if "email" not in request.json:
        return jsonify({"error" :"Missing email"}), 400
    if "password" not in request.json:
        return jsonify({"error" :"Missing password"}), 400
    kwargs = request.get_json()
    return register_new(parent_cls, None, None, kwargs)


@app_views.route(
    "/users/<user_id>",
    methods=["PUT"],
    strict_slashes=False
)
def update_user(user_id):
    """Update a user by id."""
    # validate id
    if validate_id(user_id) is False:
        return jsonify({"error" :"id is not of type uuid"}), 404
    if not request.json:
        return jsonify({"error" :"Not a valid JSON"})
    # validate if the current content exists
    get_user_obj = storage.get(parent_cls, user_id)
    if not get_user_obj:
        return jsonify({"error" :"object instance not found"}), 404
    # validate email of the obj with the 
    kwargs = request.get_json()
    print(Kwargs)
    return update_match(get_user_obj, kwargs)
  
@app_views.route(
    "/users/verify",
    methods=["POST"],
    strict_slashes=False
)
def verfiy_user():
    """Verify a user by email."""
    if not request.json:
        return jsonify({"error" :"Not a valid JSON"}), 400
    kwargs = request.get_json()
    print(kwargs)
    return validate_user(parent_cls, kwargs)

@app_views.route(
    "/users/<user_id>/tasks",
    methods=["GET"],
    strict_slashes=False
)
def user_task(user_id):
    """Get all users."""
    # validate id
    if validate_id(user_id) is False:
        return jsonify({"error" :"id is not of type uuid"}), 404
    # validate if the current user exists
    get_user_obj = storage.get(parent_cls, user_id)
    if not get_user_obj:
        return jsonify({"error" :"object instance not found"}), 404
  
    user_task = get_user_obj.tasks
    tasks = [task.to_dict() for task in user_task]
    return jsonify({"user_name": get_user_obj.name,
                    "data": tasks
                    }), 200