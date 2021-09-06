from aws_cdk import core as cdk
from aws_cdk import aws_ec2 as ec2


class VPCStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, region_name: str, env_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        subnet_configuration = [
            ec2.SubnetConfiguration(
                subnet_type=ec2.SubnetType.PUBLIC,
                name=region_name + "-sn-mediawiki-" + env_name + "-1-a",
                cidr_mask=24,
            ),
            ec2.SubnetConfiguration(
                cidr_mask=24,
                name=region_name + "-sn-mediawiki-" + env_name + "-1-b",
                subnet_type=ec2.SubnetType.PRIVATE
            )
        ]

        # Creating VPC from that subnet configuration
        self.vpc = ec2.Vpc(self, id=region_name + "-vpc-mediawiki-" + env_name, cidr='10.21.0.0/16',
                           subnet_configuration=subnet_configuration,
                           nat_gateways=1)
