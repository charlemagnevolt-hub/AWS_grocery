variable "aws_region" {
  description = "AWS region used for GroceryMate."
  type        = string
  default     = "eu-central-1"
}

variable "project_name" {
  description = "Name prefix for Terraform managed resources."
  type        = string
  default     = "grocerymate"
}

variable "owner" {
  description = "Owner tag for Terraform managed resources."
  type        = string
  default     = "Dr. Torsten Bernasco"
}

variable "lambda_function_name" {
  description = "Name of the delivery estimator Lambda function."
  type        = string
  default     = "grocerymate-delivery-estimator"
}