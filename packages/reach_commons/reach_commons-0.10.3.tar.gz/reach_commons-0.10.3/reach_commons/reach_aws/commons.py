import json

import boto3


def invoke_lambda(context, payload):
    lambda_client = boto3.client("lambda")
    lambda_client.invoke(
        FunctionName=context.function_name,
        InvocationType="Event",
        Payload=json.dumps(payload),
    )
