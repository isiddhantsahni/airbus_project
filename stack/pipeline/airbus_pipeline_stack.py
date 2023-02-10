from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions,
    aws_codebuild as codebuild
)
import aws_cdk
from constructs import Construct

class AirbusPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #Pipeline Definition

        pipeline = codepipeline.Pipeline(self, "Airbus Pipeline", pipeline_name="airbus_pipeline")

        source_output = codepipeline.Artifact()

        # Defining DEV Stage Project

        buildProject = codebuild.PipelineProject(self, 
                                                 "DEV Project", 
                                                 build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
                                                 environment= codebuild.BuildEnvironment(
                                                    build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_2
                                                 )
                                                 )

        # Adding Source Stage to pipeline through CodeStarConnectionsSourceAction

        source_stage = pipeline.add_stage(
            stage_name="Source",
            actions= [aws_codepipeline_actions.CodeStarConnectionsSourceAction(
                action_name="Source",
                owner="isiddhantsahni",
                repo="airbus_project",
                branch="DEV-01",
                connection_arn="arn:aws:codestar-connections:us-east-1:369319437787:connection/fc8e3a1a-9e77-4171-b843-e056bd6d963c",
                output=source_output
            )]
        )
        
        # Adding Build Stage

        build_stage = pipeline.add_stage(
            stage_name="Build",
            actions=[aws_codepipeline_actions.CodeBuildAction(
                action_name="Build",
                project=buildProject,
                input=source_output,
                # type=aws_codepipeline_actions.CodeBuildActionType.BUILD
            )]
        )


