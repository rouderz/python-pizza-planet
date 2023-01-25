from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, jsonify, request
from ..common import http_status_code

from ..controllers import IngredientController

class IngredientFactory:
    @staticmethod
    def create(request):
        return IngredientController.create(request.json)

    @staticmethod
    def update(request):
        return IngredientController.update(request.json)

    @staticmethod
    def get_by_id(request, _id: int):
        return IngredientController.get_by_id(_id)

    @staticmethod
    def get_all(request):
        return IngredientController.get_all()

ingredient = Blueprint('ingredient', __name__)


@ingredient.route('/', methods=POST)
def create_ingredient():
    ingredient, error = IngredientFactory.create(request)
    status_code, response = http_status_code.get_response_and_status(ingredient, error)
    return jsonify(response), status_code


@ingredient.route('/', methods=PUT)
def update_ingredient():
    ingredient, error = IngredientFactory.update(request)
    status_code, response = http_status_code.get_response_and_status(ingredient, error)
    return jsonify(response), status_code


@ingredient.route('/id/<_id>', methods=GET)
def get_ingredient_by_id(_id: int):
    ingredient, error = IngredientFactory.get_by_id(request, _id)
    status_code, response = http_status_code.get_response_and_status(ingredient, error)
    return jsonify(response), status_code


@ingredient.route('/', methods=GET)
def get_ingredients():
    ingredients, error = IngredientFactory.get_all(request)
    status_code, response = http_status_code.get_response_and_status(ingredients, error)
    return jsonify(response), status_code
