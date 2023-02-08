from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codebuild as codebuild
)
import aws_cdk
from constructs import Construct

class AirbusPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #Pipeline Definition

        pipeline = codepipeline.Pipeline(self, "Airbus Pipeline", pipeline_name="Airbus Pipeline")

        # Adding Source Stage to pipeline after creating a codebuild step

        codebuild.PipelineProject()

