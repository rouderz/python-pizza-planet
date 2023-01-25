from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request
from ..common import http_status_code

from ..controllers import SizeController

class SizeFactory:
    @staticmethod
    def create(request):
        return SizeController.create(request.json)

    @staticmethod
    def update(request):
        return SizeController.update(request.json)

    @staticmethod
    def get_by_id(request, _id: int):
        return SizeController.get_by_id(_id)

    @staticmethod
    def get_all(request):
        return SizeController.get_all()

size = Blueprint('size', __name__)


@size.route('/', methods=POST)
def create_size():
    size, error = SizeFactory.create(request)
    status_code, response = http_status_code.get_response_and_status(size, error)
    return jsonify(response), status_code


@size.route('/', methods=PUT)
def update_size():
    size, error = SizeFactory.update(request)
    status_code, response = http_status_code.get_response_and_status(size, error)
    return jsonify(response), status_code


@size.route('/id/<_id>', methods=GET)
def get_size_by_id(_id: int):
    size, error = SizeFactory.get_by_id(request, _id)
    status_code, response = http_status_code.get_response_and_status(size, error)
    return jsonify(response), status_code

@size.route('/', methods=GET)
def get_all_size():
    size, error = SizeFactory.get_all(request)
    status_code, response = http_status_code.get_response_and_status(size, error)
    return jsonify(response), status_code