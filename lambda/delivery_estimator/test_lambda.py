import importlib.util
import unittest
from pathlib import Path

module_path = Path(__file__).with_name("lambda_function.py")
spec = importlib.util.spec_from_file_location("delivery_estimator", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestDeliveryEstimator(unittest.TestCase):

    def test_standard_delivery(self):
        result = module.lambda_handler(
            {"items": [{"price": 11, "quantity": 3}]}, None
        )
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(result["body"]["total"], "37.99")

    def test_free_delivery(self):
        result = module.lambda_handler(
            {"items": [{"price": 25, "quantity": 2}]}, None
        )
        self.assertEqual(result["body"]["delivery_fee"], "0.00")
        self.assertEqual(result["body"]["total"], "50.00")

    def test_empty_cart(self):
        result = module.lambda_handler({"items": []}, None)
        self.assertEqual(result["statusCode"], 400)

    def test_negative_price(self):
        result = module.lambda_handler(
            {"items": [{"price": -5, "quantity": 1}]}, None
        )
        self.assertEqual(result["statusCode"], 400)

    def test_invalid_quantity(self):
        result = module.lambda_handler(
            {"items": [{"price": 10, "quantity": 0}]}, None
        )
        self.assertEqual(result["statusCode"], 400)


if __name__ == "__main__":
    unittest.main()
