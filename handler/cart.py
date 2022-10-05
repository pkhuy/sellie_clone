from flask import Blueprint, request, render_template, flash, redirect
from flask.json import jsonify
from flask_login import current_user
import service

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
            return render_template("cart.html")
        elif request.method == "GET":
            res = service.Cart.get_current_cart(current_user.id)
            return render_template("cart.html", context=res)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@cart_api.route('/<int:cart_id>', methods=['GET', 'POST', 'DELETE'])
def get_cart_items(cart_id):
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
            if not cart_id:
                return jsonify({"HTTP Response": 500, "content": "Internal Server"})

            return render_template(".html")
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
