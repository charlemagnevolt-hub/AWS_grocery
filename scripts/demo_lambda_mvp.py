import sys
from pathlib import Path
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "backend"))

from app.routes.delivery_routes import delivery_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "temporary-demo-only-secret"
JWTManager(app)
app.register_blueprint(delivery_bp)

client = app.test_client()

with app.app_context():
    token = create_access_token(identity="demo-user")

headers = {"Authorization": f"Bearer {token}"}

print("\n=== GROCERYMATE AWS LAMBDA DEMO ===")

print("\nTEST 1: JWT Security")
response = client.post(
    "/api/delivery/estimate",
    json={"items": [{"price": 11, "quantity": 3}]}
)
print("Without token:", response.status_code)
assert response.status_code == 401

print("\nTEST 2: Real AWS Lambda invocation")
response = client.post(
    "/api/delivery/estimate",
    json={"items": [{"price": 11, "quantity": 3}]},
    headers=headers
)
print("HTTP status:", response.status_code)
print("AWS result:", response.get_json())
assert response.status_code == 200
assert response.get_json()["total"] == "37.99"

print("\nTEST 3: Free delivery threshold")
response = client.post(
    "/api/delivery/estimate",
    json={"items": [{"price": 25, "quantity": 2}]},
    headers=headers
)
print("HTTP status:", response.status_code)
print("AWS result:", response.get_json())
assert response.status_code == 200
assert response.get_json()["delivery_fee"] == "0.00"

print("\nALL LIVE DEMO CHECKS PASSED")
