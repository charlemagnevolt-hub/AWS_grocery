import sys
from unittest.mock import patch

from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token

sys.path.insert(0, "backend")

from app.routes.delivery_routes import delivery_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "local-test-only-secret"
JWTManager(app)
app.register_blueprint(delivery_bp)

client = app.test_client()

with app.app_context():
    token = create_access_token(identity="mvp-test-user")

headers = {"Authorization": f"Bearer {token}"}

with patch(
    "app.controllers.delivery_controller.estimate_delivery",
    return_value={
        "statusCode": 200,
        "body": {
            "subtotal": "33.00",
            "delivery_fee": "4.99",
            "total": "37.99",
            "currency": "EUR"
        }
    }
):
    response = client.post(
        "/api/delivery/estimate",
        json={"items": [{"price": 11, "quantity": 3}]},
        headers=headers
    )

    print("HTTP status:", response.status_code)
    print("Response:", response.get_json())

    assert response.status_code == 200
    assert response.get_json()["total"] == "37.99"

print("Flask Lambda integration test PASSED")
