# GroceryMate Infrastructure as Code

This directory contains the Terraform configuration for the GroceryMate AWS deployment.

## Covered infrastructure

* Amazon EC2 running Amazon Linux 2023
* Application and database Security Groups
* Amazon RDS for PostgreSQL
* Private Amazon S3 avatar storage
* EC2 IAM role and instance profile
* Encrypted EBS and RDS storage
* Instance Metadata Service Version 2

## Validation

Run the following commands from this directory:

terraform init -backend=false
terraform fmt -check
terraform validate

## Important

The configuration documents the existing GroceryMate architecture.
Do not run terraform apply against the existing AWS environment before importing the existing resources into Terraform state.

Copy terraform.tfvars.example to terraform.tfvars and replace the placeholders locally.
Never commit terraform.tfvars or Terraform state files.
