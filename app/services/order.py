from app.common.http_methods import GET, POST
from flask import Blueprint, jsonify, request
from ..common import http_status_code

from ..controllers import OrderController

class OrderFactory:
    @staticmethod
    def create(request):
        return OrderController.create(request.json)

    @staticmethod
    def get_by_id(request, _id: int):
        return OrderController.get_by_id(_id)

    @staticmethod
    def get_all(request):
        return OrderController.get_all()

order = Blueprint('order', __name__)


@order.route('/', methods=POST)
def create_order():
    order, error = OrderFactory.create(request)
    status_code, response = http_status_code.get_response_and_status(order, error)
    return jsonify(response), status_code


@order.route('/id/<_id>', methods=GET)
def get_order_by_id(_id: int):
    order, error = OrderFactory.get_by_id(request, _id)
    status_code, response = http_status_code.get_response_and_status(order, error)
    return jsonify(response), status_code


@order.route('/', methods=GET)
def get_orders():
    orders, error = OrderFactory.get_all(request)
    status_code, response = http_status_code.get_response_and_status(orders, error)
    return jsonify(response), status_code
