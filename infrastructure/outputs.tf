output "ec2_instance_id" {
  description = "ID of the existing, externally managed GroceryMate EC2 instance."
  value       = data.aws_instance.existing.id
}

output "ec2_public_ip" {
  description = "Current public IP of the existing EC2 instance, if assigned."
  value       = data.aws_instance.existing.public_ip
}

output "rds_endpoint" {
  description = "Endpoint of the existing, externally managed RDS instance."
  value       = data.aws_db_instance.existing.endpoint
}

output "delivery_lambda_arn" {
  description = "ARN of the Terraform managed delivery estimator."
  value       = aws_lambda_function.delivery_estimator.arn
}