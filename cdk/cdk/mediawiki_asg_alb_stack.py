from aws_cdk import core as cdk
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import aws_elasticloadbalancingv2 as elb


class MediaWikiALBASGStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, region_name: str, env_name: str, vpc: ec2.Vpc,
                 role: iam.Role, ami_map: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        auto_scaling_group = autoscaling.AutoScalingGroup(self, id=region_name + '-asg-mediawiki-' + env_name,
                                                          instance_type=ec2.InstanceType('t2.micro'), vpc=vpc,
                                                          role=role, desired_capacity=2, max_capacity=4, min_capacity=2,
                                                          machine_image=ec2.MachineImage.generic_linux(
                                                              ami_map=ami_map),
                                                          vpc_subnets=ec2.SubnetSelection(
                                                              subnet_type=ec2.SubnetType.PRIVATE))

        mediawiki_app_alb = elb.ApplicationLoadBalancer(self,
                                                        region_name + '-lb-mediawiki-' + env_name,
                                                        http2_enabled=True,
                                                        vpc=vpc, internet_facing=True,
                                                        load_balancer_name=region_name + '-lb-mediawiki-' + env_name)

        listener_http = mediawiki_app_alb.add_listener(region_name + '-lb-mediawiki-' + env_name + '-listener-80',
                                                       port=80)
        listener_http.add_targets(id=region_name + '-tg-asg-mediawiki-' + env_name, port=80,
                                  targets=[auto_scaling_group])

        cdk.Tags.of(auto_scaling_group).add("app_type", "app_server")

        # standalone_ec2.connections.allow_from(mediawiki_app_alb,port_range=ec2.Port.tcp(80))
