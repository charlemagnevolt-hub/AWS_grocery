from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..controllers.delivery_controller import calculate_delivery

delivery_bp = Blueprint(
    "delivery",
    __name__,
    url_prefix="/api/delivery"
)

delivery_bp.route(
    "/estimate",
    methods=["POST"]
)(jwt_required()(calculate_delivery))
