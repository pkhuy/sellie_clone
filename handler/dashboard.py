from flask import Blueprint, request, render_template, flash, redirect
from flask.json import jsonify
from flask_login import current_user, login_user

import repository
import service
import jwt
import  datetime

dashboard_api = Blueprint("dashboard_api", __name__)

secret_key = 'secretaryship'

@dashboard_api.route('', methods=['GET', 'POST'])
@dashboard_api.route('/home', methods=['GET', 'POST'])
def dashboard():
    if current_user.is_authenticated:
        if request.method == "POST":
            if not request.form["name"]:
                return "Missing group name", 400
            json_data = {
                "current_user_id": current_user.id,
                "name": request.form["name"]
            }
            return render_template("dashboard.html")
        elif request.method == "GET":
            categories = repository.CategoryRepository.get_all()
            return render_template("dashboard.html", categories=categories)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@dashboard_api.route('/<int:id>', methods=['GET', 'POST', 'DELETE'])
def manage(id):
    if current_user.is_authenticated:
        if request.method == "POST":
            if request.form["act"] == "Update":
                if not request.form["name"]:
                    return "Missing group name", 400
                json_update_data = {
                    "id": id,
                    "name": request.form["name"],
                    "current_user_id": current_user.id
                }
                update_result = group_service.update(json_update_data)
                return render_template("response.html", context=update_result)
            elif request.method == "DELETE":
                delete_result = group_service.delete({
                    "id": id,
                    "current_user_id": current_user.id,
                    "entity": "group"
                })
                return render_template("response.html", context=delete_result)
        else:
            group = group_service.read_by_id(id)
            group["entity"] = "groups"
            return render_template("manage.html", context=group)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})

@dashboard_api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        if not email:
            return 'Missing Email', 401
        if not password:
            return 'Missing Password', 401
        print(request.form)
        res = service.Auth.login(request.form)

        if res is not None:
            login_user(res)
            token = jwt.encode({
                "email": request.form["email"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},
                secret_key
            )

            return redirect('/')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    else:
        return render_template('login.html')