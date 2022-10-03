from flask import Blueprint, request, render_template, flash, redirect
from flask.json import jsonify
from flask_login import current_user

import repository

cart_api = Blueprint("cart_api", __name__)



@cart_api.route('', methods=['GET', 'POST'])
def get_all():
    if current_user.is_authenticated:
        if request.method == "POST":
            if not request.form["name"]:
                return "Missing group name", 400
            json_data = {
                "current_user_id": current_user.id,
                "name": request.form["name"]
            }
            new_group = group_service.create(json_data)
            return render_template("response.html", context=new_group)
        elif request.method == "GET":
            carts = repository.CartRepository.get_carts(current_user.id)
            cart_items = repository.CartRepository
            return render_template("cart.html", carts=carts)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@cart_api.route('/<int:id>', methods=['GET', 'POST', 'DELETE'])
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