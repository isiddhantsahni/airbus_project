from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions,
    aws_codebuild as codebuild,
    aws_iam as iam
)
import aws_cdk
from constructs import Construct

from stack.resources.airbus_resources_stack import AirbusResourcesStack

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
                connection_arn="arn:aws:codestar-connections:us-east-1:369319437787:connection/53a56bf4-44d3-4c31-b432-d136b3a6185d",
                output=source_output
            )]
        )
        
        # Adding Build Stage
        build_output = codepipeline.Artifact("BuildOutput")
        build_stage = pipeline.add_stage(
            stage_name="Build",
            actions=[aws_codepipeline_actions.CodeBuildAction(
                action_name="Build",
                project=buildProject,
                input=source_output,
                outputs=[build_output],
                # type=aws_codepipeline_actions.CodeBuildActionType.BUILD
            )]
        )

        # Adding self-mutate Stage

        update_stage = aws_codepipeline_actions.CloudFormationCreateUpdateStackAction(
            action_name="Self-Mutate",
            template_path=source_output.at_path("template.yml"),
            stack_name="AirbusPipelineStack",
            admin_permissions=True,
        )

        self_mutate_stage = pipeline.add_stage(
            stage_name="Self-Mutate",
            actions=[update_stage]
        )

        
        buildProject.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=['*'],
            actions=['cloudformation:DescribeStacks',
                     'cloudformation:CreateStack',
                     'cloudformation:GetTemplate',
                     'cloudformation:DeleteChangeSet',
                     'cloudformation:CreateChangeSet',
                     'cloudformation:DescribeChangeSet',
                     'cloudformation:*',
                     'ssm:GetParameter',
                     's3:*',
                     'iam:PassRole',
                     'ec2:*'
                     ],
        ))

        dev_build = AirbusResourcesStack(self,"dev")