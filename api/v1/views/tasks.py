# #!/usr/bin/env python3
"""The blueprint for all CRUD operation for user."""
from models.task import Task
from models.user import User
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from api.v1.views import get_match, delete_match, update_match, validate_id, register_new

parent_cls = User
ch_cls = Task


@app_views.route(
    "/tasks",
    methods=["GET"],
    strict_slashes=False,
    defaults={"task_id": None},
)
@app_views.route("/tasks/<task_id>/", methods=["GET"], strict_slashes=False)
def get_task(task_id):
    """Get all Task or get a particular Task by Task id."""
    ret_data = []
    data = {}
    if task_id:
        # validate the id
        if validate_id(task_id) is False:
            return jsonify({"error" :"id is not of type uuid"}), 404
        return get_match(ch_cls, task_id)
    else:
        all_obj = storage.all(ch_cls).values()
        for obj in all_obj:
          data = {"user_name": obj.users.name, "data": obj.to_dict()}
          ret_data.append(data)
          data = {}
        return jsonify({"data": ret_data}), 200
          


@app_views.route(
    "/tasks/<task_id>",
    methods=["DELETE"],
    strict_slashes=False
)
def delete_task(task_id):
    """Delete a Task by id."""
    return delete_match(ch_cls, task_id)


@app_views.route(
    "/users/<user_id>/tasks",
    methods=["POST"],
    strict_slashes=False,
)
def create_task(user_id):
    """Create a Task via a POST request."""
    allowed_data = ["name", "start_date", "end_date", "stop_time"] 
    if not request.json:
      return  jsonify({"error" :"Not a valid JSON"}), 400
    # check if the data is valid with allowed_data
    if not all(key in request.json for key in allowed_data):
        return jsonify ({"error" :"Missing important parameters"}), 400
    kwargs = request.get_json()
    print(kwargs)
    return register_new(parent_cls, ch_cls, user_id, kwargs)


@app_views.route(
    "/tasks/<task_id>",
    methods=["PUT"],
    strict_slashes=False
)
def update_task(task_id):
    """Update a Task by id."""
    if not request.json:
      return jsonify({"error" :"Not a valid JSON"})
    # validate id
    if validate_id(task_id) is False:
        return jsonify({"error" :"id is not of type uuid"}), 404
    # validate if the current task exists
    get_task_obj = storage.get(ch_cls, task_id)
    if not get_task_obj:
        return jsonify({"error" :"object instance not found"}), 404
    kwargs = request.get_json()
    return update_match(get_task_obj, kwargs)
