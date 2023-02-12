from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3 as s3
)
from constructs import Construct

class AirbusLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #Lambda Stack
        lambda_func = _lambda.Function(
            self, "Airbus Lambda Function",
            code=_lambda.Code.from_asset('lambdas'),
            handler="listEc2Instances.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,

        )

        lambda_func.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=['*'],
            actions=[
                     'ec2:*',
                     's3:*',
                     'iam:PassRole',
                     ],
        ))

        #Import S3 Bucket
        imported_s3_bucket = s3.Bucket.from_bucket_name(self,"Airbus Bucket","airbus_bucket")

        imported_s3_bucket.grant_read_write(lambda_func)