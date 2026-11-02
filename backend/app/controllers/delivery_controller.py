from flask import jsonify, request
from ..services.delivery_service import estimate_delivery


def calculate_delivery():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({"error": "JSON object required"}), 400

    items = payload.get("items")

    if not isinstance(items, list):
        return jsonify({"error": "items must be a list"}), 400

    try:
        result = estimate_delivery(items)
        status = result.get("statusCode", 502)
        body = result.get("body", {})

        if not isinstance(body, dict):
            return jsonify({"error": "Invalid Lambda response"}), 502

        if status not in (200, 400):
            return jsonify({"error": "Lambda returned an error"}), 502

        return jsonify(body), status

    except RuntimeError:
        return jsonify({"error": "Delivery service unavailable"}), 502
