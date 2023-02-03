from aws_cdk import (
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

class AirbusEC2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #VPC