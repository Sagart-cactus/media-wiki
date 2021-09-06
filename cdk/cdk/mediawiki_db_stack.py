from aws_cdk import core as cdk
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ec2 as ec2



class MediaWikiDBStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, region_name: str, env_name: str, vpc: ec2.Vpc,
                 role: iam.Role, app_system: ec2.Instance, ami_map: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        mediawiki_db_system = ec2.Instance(self, id=region_name + '-ec-mediawiki-mysql-' + env_name + '-app-1-a',
                                            machine_image=ec2.MachineImage.generic_linux(
                                                ami_map=ami_map),
                                            vpc=vpc,
                                            instance_type=ec2.InstanceType('t2.micro'),
                                            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
                                            user_data=ec2.UserData.custom(
                                                content="""#!/bin/bash
sudo apt-get update
sudo apt-get install python3-pip
pip3 install ansible
pip3 install boto3
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i -E ./amazon-cloudwatch-agent.deb
echo '{	"agent": {		"metrics_collection_interval": 60,		"run_as_user": "cwagent"	},	"metrics": {		"append_dimensions": {			"AutoScalingGroupName": "${aws:AutoScalingGroupName}",			"ImageId": "${aws:ImageId}",			"InstanceId": "${aws:InstanceId}",			"InstanceType": "${aws:InstanceType}"		},		"metrics_collected": {			"cpu": {				"measurement": [					"cpu_usage_idle",					"cpu_usage_iowait",					"cpu_usage_user",					"cpu_usage_system"				],				"metrics_collection_interval": 60,				"totalcpu": false			},			"disk": {				"measurement": [					"used_percent",					"inodes_free"				],				"metrics_collection_interval": 60,				"resources": [					"*"				]			},			"diskio": {				"measurement": [					"io_time"				],				"metrics_collection_interval": 60,				"resources": [					"*"				]			},			"mem": {				"measurement": [					"mem_used_percent"				],				"metrics_collection_interval": 60			},			"swap": {				"measurement": [					"swap_used_percent"				],				"metrics_collection_interval": 60			}		}	}}' > config.json
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:config.json
                                          """
                                            ),
                                            role=role)

        # mediawiki_db_system.connections.allow_from(ansible_system, port_range=ec2.Port.tcp(22),
        #                                             description='Connect ansible to the mediawiki server')

        mediawiki_db_system.connections.allow_from(app_system, ec2.Port.tcp(3306))
        cdk.Tags.of(mediawiki_db_system).add("app_type", "db_server")
