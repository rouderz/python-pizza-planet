from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request
from .base import *
from ..controllers import BeverageController

beverage = Blueprint("beverage", __name__)

@beverage.route("/", methods=POST)
def create_beverage():
    return BaseSerializer.serialize(BeverageController, 'create', request)

@beverage.route("/", methods=PUT)
def update_beverage():
    return BaseSerializer.serialize(BeverageController, 'update', request)


@beverage.route("/id/<_id>", methods=GET)
def get_beverage_by_id(_id: int):
    return BaseSerializer.serialize(BeverageController, 'by_id', request, _id)


@beverage.route("/", methods=GET)
def get_all_beverage():
    return BaseSerializer.serialize(BeverageController, 'get_all', request)
