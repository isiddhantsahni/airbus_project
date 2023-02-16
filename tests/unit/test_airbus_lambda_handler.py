import aws_cdk as core
import aws_cdk.assertions as assertions

from lambdas.listEc2Instances import handler

def test_lambda_handler():
    event = {'key': 'value'}
    context = {}
    result = handler(event, context)
    assert result == {'statusCode': 200, 'body': 'File Uploaded Succesfully'}
