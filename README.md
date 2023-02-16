
# Airbus Coding Challenge

## Introduction

This is a CDK project in python, different stacks have been made for the resources, namely: EC2, Lambda, Pipeline etc.

To add the CI/CD aspect to the project, AWS CodePipeline was used. 

A connection with the github repo had to be made so that whenever a new commit is made to the mentioned branch, it can trigger the codepipeline (Through webhooks). The new changes will be used for SelfMutate step of the codepipeline and be updated for the application. Through this, the devs can continuously develop the application and continuously integrate it through codebuild as well(Used in the project).

## Architecture

![CodePipeline Project Arch](https://github.com/isiddhantsahni/airbus_project/blob/DEV-01/images/Codepipeline.png)

![Application Architecture](https://github.com/isiddhantsahni/airbus_project/blob/DEV-01/images/Application%20Architecture.png)

## Deploying the project to any AWS Account

Prerequisites:
Install aws cdk, aws cli, python, git, node to run the project.

1. Clone the repo into your development environment using:
```
$ git clone https://github.com/isiddhantsahni/airbus_project.git
```
[Then push the git repo to your own account]

2. Run ```cdk bootstrap aws://ACCOUNT-NUMBER/REGION``` (If the aws account already hasn't been bootstraped, do this through the command mentioned. Deploying stacks with the AWS CDK requires dedicated Amazon S3 buckets and other containers to be available to AWS CloudFormation during deployment. Creating these is called bootstrapping.)

3. Create a connection with your github repo in AWS CodePipeline:

![CodePipeline Connection](https://github.com/isiddhantsahni/airbus_project/blob/DEV-01/images/Connection.PNG)

Click Create connection, choose GitHub, mention any name. Next, Click on Install a new app, and at the end choose connect. You'll see a connection made like below:

![CodePipeline Connection](https://github.com/isiddhantsahni/airbus_project/blob/DEV-01/images/Connection1.PNG)

[Replace the connection ARN in the source stage in the pipeline stack. Also replace other parameters.]

```python
source_stage = pipeline.add_stage(
            stage_name="Source",
            actions= [aws_codepipeline_actions.CodeStarConnectionsSourceAction(
                action_name="Source",
                owner="isiddhantsahni",
                repo="airbus_project",
                branch="DEV-01",
                connection_arn="arn:aws:codestar-connections:us-east-1:36911111111:connection/fc8e3a1a-9e77-4171-b843-e056bd6d963c",
                output=source_output
            )]
        )
```

4. RUN ```aws configure``` and set the access key and other parameters.

5. In app.py replace the account number and region for your account.

![App.py Environment](https://github.com/isiddhantsahni/airbus_project/blob/DEV-01/images/environment.PNG)

6. RUN ```cdk deploy AirbusPipelineStack``` in command line in the respective IDE to deploy the application.(Eg. Visual Studio Code)

[After the codepipeline runs successfully, the lambda function will run each day at 12PM UTC and save the csv file to the s3 bucket. Any further commits to the branch will trigger the pipeline for auto updation.]

## CodePipeline Image
![Codepipeline](https://github.com/isiddhantsahni/airbus_project/blob/DEV-01/images/CodePipeline_img.png)

After successfully running.

## Lambda Function
![Lambda](https://github.com/isiddhantsahni/airbus_project/blob/DEV-01/images/Lambda_Function.PNG)

## S3 Location
![s3](https://github.com/isiddhantsahni/airbus_project/blob/DEV-01/images/s3.PNG)


## CSV File Example
![ec2-inventory-latest.csv](https://github.com/isiddhantsahni/airbus_project/blob/DEV-01/images/csv.PNG)

## Test Cases
To run test cases on local run command ```pytest```

In buildspec.yml file, the post-build step contains the ```pytest``` command to run the unit test cases in the ```\tests``` folder.

![Postbuild](https://github.com/isiddhantsahni/airbus_project/blob/DEV-01/images/buildspec_postbuild.PNG)

Below is the CodeBuild logs for the end which showcases the test cases running successfully.
![CodeBuild_test](https://github.com/isiddhantsahni/airbus_project/blob/DEV-01/images/CodeBuild_Test.PNG)
