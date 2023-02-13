from aws_cdk import (
    Stack,
)
from constructs import Construct
from stack.ec2.airbus_ec2_stack import AirbusEC2Stack
from stack.s3.airbus_s3_stack import AirbusS3Stack
from stack.lambdas.airbus_lambda_stack import AirbusLambdaStack

class AirbusResourcesStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        airbus_ec2_stack = AirbusEC2Stack(self,"AirbusEC2Stack")

        airbus_s3_stack = AirbusS3Stack(self,"AirbusS3Stack")

        airbus_lambda_stack = AirbusLambdaStack(self,"AirbusLambdaStack")

        