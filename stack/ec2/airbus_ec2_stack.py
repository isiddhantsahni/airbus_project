from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct

class AirbusEC2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #VPC
        vpc = ec2.Vpc(self,"Airbus VPC for EC2")
        #,subnet_configuration=ec2.SubnetConfiguration(cidr_mask=24, name='Ingress', subnet_type=ec2.SubnetType.PRIVATE_ISOLATED)

        #Security Group
        my_security_group = ec2.SecurityGroup(self, "Airbus Security Group",
            vpc=vpc,
            security_group_name="Airbus Security Group",
            description="Allow ssh access to ec2 instances",
            allow_all_outbound=True
        )
        my_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow ssh access from the world")

        # AWS Linux EC2 Instance
        ec2.Instance(self, "Instance1",
            vpc=vpc,
            security_group=my_security_group,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
            machine_image=ec2.AmazonLinuxImage()
        )

        # AWS Linux 2 EC2 Instance
        ec2.Instance(self, "Instance2",
            vpc=vpc,
            security_group=my_security_group,
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T2, ec2.InstanceSize.MICRO),
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
            )
        )
