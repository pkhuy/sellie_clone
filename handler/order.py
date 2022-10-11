from flask import Blueprint, request, render_template, flash, redirect
from flask.json import jsonify
from flask_login import current_user

import service

order_api = Blueprint("order_api", __name__)



@order_api.route('', methods=['GET', 'POST'])
def get_all():
    if current_user.is_authenticated:
        if request.method == "POST":
            return render_template("response.html", context=new_group)
        elif request.method == "GET":
            orders = service.Order.get_current_user_orders(current_user.id)

            return render_template("orders.html", context=orders)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})


@order_api.route('/<int:order_id>', methods=['GET', 'POST', 'DELETE'])
def get_detail(order_id):
    if current_user.is_authenticated:
        if request.method == "POST":

            return render_template("order.html")
        else:
            order = service.Order.get_order_detail(order_id)
            return render_template("manage.html", context=order)
    else:
        return jsonify({"HTTP Response": 204, "content": "U must login"})
