from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INFRA = ROOT / "infrastructure"

class TestTerraformMVP(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.main = (INFRA / "main.tf").read_text(encoding="utf-8")
        cls.lambda_tf = (INFRA / "lambda.tf").read_text(encoding="utf-8")
        cls.variables = (INFRA / "variables.tf").read_text(encoding="utf-8")

    def test_lambda_managed_by_terraform(self):
        self.assertIn('resource "aws_lambda_function" "delivery_estimator"', self.lambda_tf)
        self.assertIn("source_code_hash", self.lambda_tf)

    def test_ec2_lambda_permission(self):
        self.assertIn("lambda:InvokeFunction", self.lambda_tf)
        self.assertIn("aws_lambda_function.delivery_estimator.arn", self.lambda_tf)

    def test_region_configuration(self):
        self.assertIn('default     = "eu-central-1"', self.variables)
        self.assertNotIn('region = "us-east-1"', self.lambda_tf)

    def test_pinned_ami(self):
        self.assertIn("ami                    = var.ec2_ami_id", self.main)
        self.assertNotIn("most_recent = true", self.main)

    def test_deployment_trigger(self):
        self.assertIn("user_data_replace_on_change = true", self.main)

    def test_rds_instance_variable(self):
        self.assertIn("instance_class              = var.db_instance_class", self.main)

if __name__ == "__main__":
    unittest.main(verbosity=2)
