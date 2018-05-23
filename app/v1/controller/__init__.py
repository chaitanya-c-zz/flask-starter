from flask import Blueprint

from app.v1.controller.status_controller import StatusController

v1_blueprint = Blueprint('v1', __name__)

StatusController.register(v1_blueprint, route_base='/')
