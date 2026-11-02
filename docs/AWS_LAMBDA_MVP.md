# GroceryMate AWS Lambda MVP

## Overview

This project extends the existing GroceryMate Flask application
with an AWS Lambda delivery cost estimator.

The original PostgreSQL database and existing product endpoints
remain unchanged.

## Architecture

Client
  -> Flask API
  -> JWT Authentication
  -> Delivery Controller
  -> Delivery Service (boto3)
  -> AWS Lambda
  -> Calculation Result

## AWS Configuration

Region: us-east-1
Lambda function: grocerymate-delivery-estimator
Runtime: Python 3.12
Handler: lambda_function.lambda_handler

## API Endpoint

POST /api/delivery/estimate

Authentication: JWT Bearer token required.

Example request:

{
  "items": [
    {"price": 11, "quantity": 3}
  ]
}

Successful response:

{
  "subtotal": "33.00",
  "delivery_fee": "4.99",
  "total": "37.99",
  "currency": "EUR"
}

## Business Logic

Orders below EUR 50 incur a EUR 4.99 delivery fee.
Orders of EUR 50 or more receive free delivery.

Invalid input is rejected.

Prices are demonstration inputs and are not independently
verified against the product database.

## Local Setup

Install dependencies from backend/requirements.txt.

Use an AWS profile with permission to invoke the Lambda function.

Example PowerShell configuration:

$env:AWS_PROFILE = "grocerymate"
$env:AWS_DEFAULT_REGION = "us-east-1"

No permanent AWS credentials are stored in the source code.

## Testing

Five Lambda unit tests passed.

The isolated Flask integration test passed using a mocked
Lambda response.

A real boto3 invocation of the deployed AWS Lambda function passed.

A full Flask route test using the real AWS Lambda function passed:

Unauthenticated request: HTTP 401
Authenticated request: HTTP 200
Calculated total: EUR 37.99

Python dependency verification passed with pip check.

## Scope and Limitations

The Lambda function is deployed and integrated with the
Flask backend.

The complete application startup and React frontend integration
have not yet been verified.

The production runtime must have IAM permission to invoke Lambda.
A dedicated least-privilege IAM role is recommended.

The implementation is an educational MVP, not a production
checkout or payment solution.
