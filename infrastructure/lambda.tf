data "archive_file" "delivery_lambda" {
  type        = "zip"
  source_file = "${path.module}/../lambda/delivery_estimator/lambda_function.py"
  output_path = "${path.module}/delivery_lambda.zip"
}

resource "aws_iam_role" "lambda_execution" {
  name = "${var.project_name}-delivery-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_logging" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_cloudwatch_log_group" "delivery_lambda" {
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = 7
}

resource "aws_lambda_function" "delivery_estimator" {
  function_name    = var.lambda_function_name
  role             = aws_iam_role.lambda_execution.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.12"
  filename         = data.archive_file.delivery_lambda.output_path
  source_code_hash = data.archive_file.delivery_lambda.output_base64sha256
  timeout          = 10
  memory_size      = 128

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logging,
    aws_cloudwatch_log_group.delivery_lambda
  ]
}

resource "aws_iam_role_policy" "lambda_invoke" {
  name = "${var.project_name}-lambda-invoke"
  role = aws_iam_role.ec2.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["lambda:InvokeFunction"]
      Resource = aws_lambda_function.delivery_estimator.arn
    }]
  })
}
