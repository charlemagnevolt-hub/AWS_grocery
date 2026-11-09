# GroceryMate Terraform Scope

## Current scope

This Terraform root manages the deployed GroceryMate delivery estimator
Lambda integration and the existing EC2 IAM role.

The configuration was reconciled with the real AWS environment rather
than creating a second, unused application infrastructure stack.

## Managed resources

- Delivery estimator Lambda function
- Lambda execution IAM role
- Lambda logging policy attachment
- CloudWatch log group
- Existing EC2 IAM role, imported as `aws_iam_role.existing_ec2`
- Lambda invoke permission on the existing EC2 IAM role
- SSM managed policy attachment on the existing EC2 IAM role

The existing EC2 IAM role is `GroceryMateWeek7S3Role`.

Its original S3 access policy remains in place.

## Referenced existing infrastructure

The following resources are read through Terraform data sources and
are not managed by this Terraform root:

- EC2 instance: `i-0d3f05f49de3c67b1`
- RDS database: `database-1`

The existing S3 bucket
`grocerymate-week7-torsten-683554602189`
is also outside the managed resource scope.

The existing EC2 and RDS instances are not recreated or modified
by this configuration.

## Validation

After the IAM role import:

- `terraform validate -no-color` completed successfully.
- `terraform plan -input=false -no-color` reported no changes.
- No additional EC2 or RDS resources were planned.
- The imported role is present in `terraform state list`.

## Limitation

This is a scoped Terraform configuration, not a claim that the complete
legacy GroceryMate environment is managed as infrastructure as code.

Full management of the existing EC2, RDS, networking and S3 resources
would require separately reviewed imports and configuration alignment.