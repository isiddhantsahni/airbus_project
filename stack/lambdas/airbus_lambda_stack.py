from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3 as s3,
    aws_events as events,
    aws_events_targets as event_targets
)
import aws_cdk as cdk
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
            function_name="airbus-lambda-function",
            timeout=cdk.Duration.minutes(1)
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
        imported_s3_bucket = s3.Bucket.from_bucket_name(self,"Airbus Bucket","airbus-final-bucket")

        imported_s3_bucket.grant_read_write(lambda_func)

        #Creating Event Rule to trigger Lambda Function

        lambda_rule = events.Rule(self,
                    "Event Rule for Lambda Function",
                    description= "Event Rule to trigger the Airbus Lambda Function",
                    #Scheduled for 12PM UTC Each day
                    # schedule=events.Schedule.cron(minute="0",hour="12",day="*",month="*",year="*"),
                    schedule=events.Schedule.rate(cdk.Duration.minutes(5)),
                    targets=[event_targets.LambdaFunction(lambda_func)]
                    )
