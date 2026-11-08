# GroceryMate AWS Lambda MVP
## Technical Validation and Handover

**Validation date:** 2026-11-08
**AWS region:** eu-central-1
**Git branch:** feature/aws-lambda-mvp
**Status:** Lambda MVP validated. EC2 application deployment pending.

## 1. Executive Summary

The GroceryMate delivery estimation Lambda was successfully
deployed through Terraform and tested against AWS.

The existing EC2 instance successfully invoked the Lambda
using its assigned IAM role.

The current Flask integration was also tested locally,
including JWT-protected API requests.

The remaining work is to deploy the current Flask application
revision to EC2 and validate the complete HTTP request path.

## 2. AWS Infrastructure

AWS account: 683554602189

Lambda function:
grocerymate-delivery-estimator

Lambda ARN:
arn:aws:lambda:eu-central-1:683554602189:function:grocerymate-delivery-estimator

Existing EC2 instance:
i-0d3f05f49de3c67b1

EC2 instance profile:
GroceryMateWeek7S3Role

Terraform backend:
S3 remote state with encryption, versioning and state locking.

EC2 final state:
stopped

RDS:
not started during the integration test.

## 3. Verified Results

### 3.1 Lambda invocation

Input:
- Price: EUR 11.00
- Quantity: 3

Observed output:
- Subtotal: EUR 33.00
- Delivery fee: EUR 4.99
- Total: EUR 37.99
- Currency: EUR

AWS Lambda invocation status: 200
Lambda response statusCode: 200

### 3.2 IAM and EC2

The existing EC2 instance successfully assumed:

arn:aws:sts::683554602189:assumed-role/GroceryMateWeek7S3Role/i-0d3f05f49de3c67b1

The instance directly invoked the Frankfurt Lambda function.

The IAM simulation also confirmed the required Systems Manager
permissions.

### 3.3 Systems Manager

SSM registration: Online
Operating system: Amazon Linux
SSM agent version: 3.3.4624.0

Remote inspection and Lambda testing through SSM succeeded.

### 3.4 Local Flask integration

Previously validated:
- Unauthorized JWT request returns HTTP 401.
- Authorized delivery request returns HTTP 200.
- Delivery fee and free-delivery cases pass.

This validation was performed locally, not on the existing
EC2 application deployment.

## 4. Existing EC2 Application Findings

The legacy application runs from:

/home/ec2-user/AWS_grocery/backend

Gunicorn binds to port 5000.

The HTTP root endpoint returns status 200.

A separate Docker container named backend also attempts
to bind port 5000 using host networking.

This causes a port conflict and a container restart loop.

The existing application installation does not contain:
- backend/app/services/delivery_service.py
- backend/app/routes/delivery_routes.py

Therefore the new delivery API has not yet been deployed
to the existing EC2 application environment.

A Git ownership warning prevented confirmation of the
installed repository revision.

## 5. Outstanding Work

1. Establish the intended EC2 deployment method.
2. Inspect the legacy Gunicorn and Docker startup configuration.
3. Resolve the duplicate port 5000 binding.
4. Deploy a reviewed application revision to EC2.
5. Configure the required Lambda function name and AWS region.
6. Validate the JWT-protected delivery API over HTTP on EC2.
7. Verify the end-to-end Lambda response through Flask.
8. Stop EC2 again after testing to control costs.

No legacy application processes were intentionally replaced
or stopped during this validation.

## 6. Deployment Safety

Do not run an unrestricted Terraform apply against the
existing AWS environment.

The current Terraform state does not manage every resource
declared in the infrastructure configuration.

A full apply may attempt to provision additional EC2 or
database resources.

Existing EC2 and RDS infrastructure must be preserved.

## 7. Conclusion

Validated:
- Terraform-managed AWS Lambda deployment
- Remote Terraform state
- Direct Lambda invocation
- Local Flask and JWT integration
- EC2 IAM permissions
- Real EC2-to-Lambda invocation
- SSM remote access

Pending:
- Updated Flask application deployment on EC2
- Complete EC2 HTTP integration test

The Lambda MVP is validated at the infrastructure and
service integration levels, but the complete deployed
application path remains unverified.
