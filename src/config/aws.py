import boto3
import os
import botocore as bt
from boto3.dynamodb.conditions import Key, Attr
import botocore.exceptions

# our global configuration
configuration = bt.config.Config(
    region_name="us-east-2",
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)


class Services:
    dynamodb = boto3.resource("dynamodb", config=configuration)
    cognito = boto3.client("cognito-idp")
    cognito_id = boto3.client("cognito-identity")
    s3 = boto3.client("s3")
    bucket_name = "file-storage-global113245-dev"
