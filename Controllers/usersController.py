from werkzeug.security import check_password_hash
from forms.registerform import RegisterForm
from forms.updateform import UpdateForm
from forms.loginform import LoginForm
from flask import request, jsonify
from Models.Model import Model
import sqlite3

def get_all_users():
    return jsonify(Model.where("users")),200

def create_user() :
    data = request.get_json() 
    username = data["username"]
    email = data["email"]
    password = data["password"]
    password_conf = data["confirm-password"]
    validate_form = RegisterForm(username,email,password,password_conf)
        
    validate_form.validate()
    if validate_form.is_valid():
        info = Model.where("users","email",email)
        if len(info)!=0 :
            return jsonify({ "errors": {"email":'Email already used'} }),422 
        else :
            info = {"username":username,"email": email,"password": password}
            id = Model.create("users",info)
            return jsonify(Model.where("users","id",id)), 201
    else :
        return jsonify({"errors": validate_form.errors}),400

def log_user():
    data = request.get_json() 
    email = data["email"]
    password = data["password"]
    
    validate_form = LoginForm(email,password)
    validate_form.validate()
    if validate_form.is_valid() :
        response = Model.where("users","email",email)
        if len(response) == 0 :
            return jsonify({ "errors": {"email": 'Incorrect email'} }),422             
        else :
            if not check_password_hash(response["password"],password):
                return jsonify({ "errors": {"password": 'Incorrect password'}}),422
            else :
                return jsonify({"message":"User logged successfully", "user":response}),200
    else :
        return jsonify({"errors":validate_form.errors}),400
    


def read_user(id):
    info = Model.where("users","id",id)
    if len(info)!=0:
        return jsonify(Model.where("users","id",id)),200
    else :
        return jsonify({"errors":"User not found"}),404

def update_user(id):
    data = request.get_json()
    new_username = data["username"]
    new_email = data["email"]
    validate_form = UpdateForm(new_username,new_email)
    validate_form.validate()
    if validate_form.is_valid() :
        info = Model.where("users","id",id)
        if len(info)!=0:
            if new_email != info["email"]:
                try :
                    Model.update("users","email",id,new_email)
                except sqlite3.IntegrityError as e :
                    return jsonify({ "errors": {"email": 'Email already used'} }),422 
            Model.update("users","username",id,new_username)
            return jsonify({"message": "User updated successfully"}),200
        else :
            return jsonify({"errors":"User not found"}),404
    else :
        return jsonify({"errors":validate_form.errors}),400

def delete_user(id):
    info = Model.where("users","id",id)
    if len(info)!=0:
        Model.delete("users",id)
        return jsonify({"message":"User deleted"}),200
    else :
        return jsonify({"errors":"User not found"}),404