from app.common.http_methods import GET, POST
from flask import Blueprint, request
from .base import *

from ..controllers import OrderController

order = Blueprint('order', __name__)


@order.route('/', methods=POST)
def create_order():
    return BaseSerializer.serialize(OrderController, 'create', request)


@order.route('/id/<_id>', methods=GET)
def get_order_by_id(_id: int):
    return BaseSerializer.serialize(OrderController, 'by_id', request, _id)


@order.route('/', methods=GET)
def get_orders():
    return BaseSerializer.serialize(OrderController, 'get_all', request)
