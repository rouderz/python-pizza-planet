from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request
from ..controllers import BeverageController
from ..common import http_status_code

class BeverageFactory:
    @staticmethod
    def create(request):
        return BeverageController.create(request.json)

    @staticmethod
    def update(request):
        return BeverageController.update(request.json)

    @staticmethod
    def get_by_id(request, _id: int):
        return BeverageController.get_by_id(_id)

    @staticmethod
    def get_all(request):
        return BeverageController.get_all()

beverage = Blueprint("beverage", __name__)

@beverage.route("/", methods=POST)
def create_beverage():
    beverage, error = BeverageFactory.create(request)
    status_code, response = http_status_code.get_response_and_status(beverage, error)
    return jsonify(response), status_code

@beverage.route("/", methods=PUT)
def update_beverage():
    beverage, error = BeverageFactory.update(request)
    status_code, response = http_status_code.get_response_and_status(beverage, error)
    return jsonify(response), status_code

@beverage.route("/id/<_id>", methods=GET)
def get_beverage_by_id(_id: int):
    beverage, error = BeverageFactory.get_by_id(request, _id)
    status_code, response = http_status_code.get_response_and_status(beverage, error)
    return jsonify(response), status_code

@beverage.route("/", methods=GET)
def get_all_beverage():
    beverage, error = BeverageFactory.get_all(request)
    status_code, response = http_status_code.get_response_and_status(beverage, error)
    return jsonify(response), status_code