from aws_cdk import (
    Stack
)
import aws_cdk
from constructs import Construct

class AirbusPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #Pipeline

        