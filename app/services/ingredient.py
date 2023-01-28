from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request
from .base import * 

from ..controllers import IngredientController

ingredient = Blueprint('ingredient', __name__)


@ingredient.route('/', methods=POST)
def create_ingredient():
    return BaseServices.serialize(IngredientController, 'create', request)


@ingredient.route('/', methods=PUT)
def update_ingredient():
    return BaseServices.serialize(IngredientController, 'update', request)


@ingredient.route('/id/<_id>', methods=GET)
def get_ingredient_by_id(_id: int):
   return BaseServices.serialize(IngredientController, 'by_id', request, _id)


@ingredient.route('/', methods=GET)
def get_ingredients():
    return BaseServices.serialize(IngredientController, 'get_all', request)
