#!/usr/bin/env python3
"""model for blue print view"""
from flask import Blueprint, make_response, jsonify
from models import storage
from models.user import User
from models.task import Task
import bcrypt
import uuid

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


def get_match(cls, id):
    """GET: get the object of a specific class based on its id"""
    # validate the id
    if validate_id(id) is False:
        return jsonify({"error" :"id is not of type uuid"}), 404
    obj = storage.get(cls, id)
    if obj:
        if obj.__class__.__name__ == "User":
            return jsonify({"data": obj.to_dict()}), 200
        elif obj.__class__.__name__ == "Task":
            name = obj.users.name
            return jsonify({"user_name": name,
                        "data": obj.to_dict()
                        }), 200
    return jsonify({"error" :"Object not found"}), 404



def delete_match(cls, id):
    """DELETE: delete the object of a specific class based on its id"""
    # validate the id
    if validate_id(id) is False:
        return jsonify({"error" :"id is not of type uuid"}), 404
    obj = storage.get(cls, id)
    if obj:
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({"message" :"Object deleted successfully"}), 200)
    return jsonify({"error" :"Object not found"}), 404


def register_new(p_cls, ch_cls, p_id, kwargs):
    print('hhhhhhhhhhhhhh')
    """POST: creating a new object for the class"""
    # validate if the id is associated with any object in the User table
    if p_cls == User and ch_cls is None:
        # validate if the current content exists
        all_obj = storage.all(p_cls).values()
        for obj in all_obj:
            if obj.email == kwargs["email"]:
                return jsonify ({"error" :"User and email already exists"}), 400
        if "password" in kwargs:
          password = kwargs["password"]
          hash_pswd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
          kwargs["password"] = hash_pswd
        obj = p_cls(**kwargs)
        obj.save()
        return get_match(p_cls, obj.id)
    elif p_cls == User and ch_cls == Task:
        # validate the id first
        if validate_id(p_id) is False:
            return jsonify({"error" :"id is not of type uuid"}), 404
        # validate the user if it exists        
        user = storage.get(User, p_id)
        if user is None:
            return jsonify({"error" :"User not found"}), 404
        # validate if the current task already exists
        all_obj = storage.all(ch_cls).values()
        for obj in all_obj:
            if obj.name == kwargs["name"] and obj.user_id == p_id:
                return jsonify ({"error" :"Task name already exists"}), 400
        # create a new object instance for the task class
        # add the user_id 
        kwargs["user_id"] = p_id
        obj = ch_cls(**kwargs)
        obj.save()
        return jsonify({"message": "task created successfully",
                        "data": obj.to_dict()
                        }), 201
    else:
        return jsonify({"error" :"Object not found"}), 404


def update_match(obj, kwargs):
    """PUT: update the brand object"""
    if "password" in kwargs:
      password = kwargs["password"]
      hash_pwsd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
      kwargs["password"] = hash_pwsd
    for key, value in kwargs.items():
      setattr(obj, key, value)   
    obj.save()
    ret_data = jsonify(obj.to_dict())
    return make_response(ret_data, 200)
  
  
def validate_user(p_cls, kwargs):
    """POST: validate the user credentials"""
    if "email" not in kwargs:
        return jsonify ({"error" :"Missing email"}), 400        
    if "password" not in kwargs:
        return jsonify ({"error" :"Missing password"}), 400
    # validate if the current content exists
    all_obj_users = storage.all(p_cls).values()
    # validate if the email exists
    email = kwargs["email"]
    for obj in all_obj_users:
        if obj.email == email:
            # validate the password
            if bcrypt.checkpw(kwargs["password"].encode('utf-8'), obj.password.encode('utf-8')):            
                # password is valid
                return jsonify ({"login": "Successful", "id": obj.id}), 201
            else:
                # password is invalid
                return jsonify ({"error" :"Invalid password"}), 400
        else:
          continue
    else:
      return jsonify ({"error" :"User not found"}), 404
      
def validate_id(id):
  # Try to create a UUID object from the input string
  try:
    if uuid.UUID(id, version=4):
      return True
  except ValueError:
    return False
  
  
def class_id(cls, id):
  # check if the id is associated with the class
  obj = storage.get(cls, id)
  if obj:
    return True
  else:
    return False

# used to instantiate the blueprint routes upon program start-up
from api.v1.views.users import *
from api.v1.views.tasks import *