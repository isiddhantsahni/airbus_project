from aws_cdk import (
    Stack,
    aws_s3 as s3
)
import aws_cdk as cdk
from constructs import Construct

class AirbusS3Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #S3 Stack
        s3.Bucket(self,
                  "Airbus Bucket",
                  auto_delete_objects=True,
                  bucket_name="airbus-final-bucket",
                  removal_policy=cdk.RemovalPolicy.DESTROY,
                  )