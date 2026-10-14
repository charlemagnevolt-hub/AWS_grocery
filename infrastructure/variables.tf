variable "aws_region" {
  description = "AWS region used for the GroceryMate deployment."
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Name prefix for AWS resources."
  type        = string
  default     = "grocerymate"
}

variable "instance_type" {
  description = "EC2 instance type."
  type        = string
  default     = "t3.small"
}

variable "key_name" {
  description = "Existing EC2 key pair name."
  type        = string
  default     = "grocerymate-week2-key"
}

variable "allowed_ssh_cidr" {
  description = "Trusted client address for SSH access."
  type        = string
  default     = "0.0.0.0/32"
}

variable "allowed_app_cidr" {
  description = "Trusted client address for GroceryMate access."
  type        = string
  default     = "0.0.0.0/0"
}

variable "db_username" {
  description = "PostgreSQL administrator username."
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "PostgreSQL administrator password."
  type        = string
  sensitive   = true
}

variable "s3_bucket_name" {
  description = "Globally unique private S3 bucket name."
  type        = string
  default     = "grocerymate-week7-torsten-683554602189"
}
