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
                                                 build_spec=codebuild.BuildSpec.from_source_filename("pipeline/buildspec.yml"),
                                                # build_spec= codebuild.BuildSpec.from_object(
                                                #     {
                                                #         "version": "0.2",
                                                #         "phases": {
                                                #             "install": {
                                                #                 "runtime-versions": {"nodejs": "14"}
                                                #             }, 
                                                #             "pre_build":{
                                                #                 "commands": [
                                                #                     "npm install -g aws-cdk",
                                                #                     "npm install",
                                                #                     "pip install -r requirements.txt",
                                                #                     "node --version",
                                                #                 ]
                                                #             },
                                                #             "build": {
                                                #                 "commands": [
                                                #                     "echo Hello, World!",
                                                #                     "echo Build started on `date`",
                                                #                     "cdk deploy",
                                                #                 ]
                                                #             },
                                                #             "post_build": {
                                                #                 "commands": [
                                                #                     "echo Build completed on `date`",
                                                #                 ]
                                                #             },
                                                #         },
                                                #     }
                                                # ),
                                                 environment= codebuild.BuildEnvironment(
                                                            build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
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


