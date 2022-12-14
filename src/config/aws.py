import boto3
import os
import botocore as bt
from boto3.dynamodb.conditions import Key, Attr
import botocore.exceptions
from dotenv import load_dotenv

load_dotenv()

USER_POOL_ID = os.getenv("USER_POOL_ID")
BUCKET_ID = os.getenv("BUCKET_NAME")
QUEUE_URL= os.getenv("QUEUE_URL")
AWS_REGION = "us-east-2"

# our global configuration
configuration = bt.config.Config(
    region_name= AWS_REGION,
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)


class Services:
    queue_url = QUEUE_URL
    dynamodb = boto3.resource("dynamodb", config=configuration)
    cognito = boto3.client("cognito-idp", region_name = AWS_REGION )
    cognito_id = boto3.client("cognito-identity", region_name = AWS_REGION)
    s3 = boto3.resource("s3")
    client_3 = boto3.client("s3", region_name = AWS_REGION)
    s3_bucket = s3.Bucket(BUCKET_ID)
    bucket_name = BUCKET_ID
    sqs = boto3.client("sqs", region_name = AWS_REGION)
