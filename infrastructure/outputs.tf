output "ec2_instance_id" {
  description = "ID of the GroceryMate EC2 instance."
  value       = aws_instance.application.id
}

output "ec2_public_ip" {
  description = "Public IP address of the GroceryMate EC2 instance."
  value       = aws_instance.application.public_ip
}

output "rds_endpoint" {
  description = "Private Amazon RDS endpoint."
  value       = aws_db_instance.database.endpoint
}

output "s3_bucket_name" {
  description = "Private S3 bucket used for GroceryMate avatars."
  value       = aws_s3_bucket.avatars.bucket
}
