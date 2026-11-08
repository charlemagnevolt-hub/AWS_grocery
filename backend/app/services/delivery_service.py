import json
import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def estimate_delivery(items):
    function_name = os.getenv(
        "DELIVERY_LAMBDA_NAME",
        "grocerymate-delivery-estimator"
    )
    region = os.environ["AWS_DEFAULT_REGION"]

    client = boto3.client("lambda", region_name=region)

    try:
        response = client.invoke(
            FunctionName=function_name,
            InvocationType="RequestResponse",
            Payload=json.dumps({"items": items}).encode("utf-8")
        )
        result = json.loads(response["Payload"].read())

        if response.get("FunctionError"):
            raise RuntimeError("Lambda execution failed")

        if not isinstance(result, dict):
            raise RuntimeError("Unexpected Lambda response")

        return result

    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError("AWS Lambda invocation failed") from exc
