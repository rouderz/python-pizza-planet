from app.common.http_methods import GET
from flask import Blueprint, request
from .base import *


from ..controllers import ReportController

report = Blueprint('report', __name__)


@report.route('/', methods=GET)
def get_report():
    return BaseServices.serialize(ReportController, 'get_report', request)