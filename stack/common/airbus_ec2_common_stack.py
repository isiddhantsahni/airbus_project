from aws_cdk import (
    Stack,
    aws_ec2 as _ec2,
    aws_lambda as _lambda,
    CfnOutput as cfn
    
)
import aws_cdk
from constructs import Construct

class AirbusCommonStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #VPC
        _vpc = _ec2.Vpc(self, "Airbus VPC", subnet_configuration=_ec2.SubnetConfiguration(cidr_mask=24, name='Ingress', subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED))

        #Security Group
        security_group = _ec2.SecurityGroup(self, "Airbus Security Group", vpc=_vpc, security_group_name="Airbus Security Group")

        vpc_export = cfn(self,"vpc export", export_name="", value=_vpc.vpc_arn)
        
        _ec2.Vpc.from_vpc_attributes(self,"Airbus VPC", )
        aws_cdk.Fn.import_value()

        