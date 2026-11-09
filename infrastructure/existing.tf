# Existing infrastructure is not managed by this Lambda stack.
# These data sources identify the live GroceryMate environment.
# No EC2 or RDS creation is performed by this configuration.

data "aws_instance" "existing" {
  instance_id = "i-0d3f05f49de3c67b1"
}

data "aws_db_instance" "existing" {
  db_instance_identifier = "database-1"
}
# Existing EC2 IAM role, to be adopted without replacing it.
resource "aws_iam_role" "existing_ec2" {
  provider             = aws.existing
  name                 = "GroceryMateWeek7S3Role"
  path                 = "/"
  description          = "Allows the GroceryMate EC2 instance to access its Week 7 S3 bucket."
  max_session_duration = 3600

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })

  lifecycle {
    prevent_destroy = true
  }
}

import {
  to = aws_iam_role.existing_ec2
  id = "GroceryMateWeek7S3Role"
}