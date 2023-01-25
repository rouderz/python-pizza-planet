from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request
from .base import *

from ..controllers import SizeController

size = Blueprint('size', __name__)


@size.route('/', methods=POST)
def create_size():
    return BaseSerializer.serialize(SizeController, 'create', request)


@size.route('/', methods=PUT)
def update_size():
    return BaseSerializer.serialize(SizeController, 'update', request)


@size.route('/id/<_id>', methods=GET)
def get_size_by_id(_id: int):
    return BaseSerializer.serialize(SizeController, 'by_id', request, _id)

@size.route('/', methods=GET)
def get_all_size():
    return BaseSerializer.serialize(SizeController, 'get_all', request)