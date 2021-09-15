#!/usr/bin/env python3
import os

from aws_cdk import core as cdk
from vpc_stack import VPCStack
from iam_stack import IamStack
from mediawiki_app_stack import MediaWikiStack
from deployment_S3 import DeploymentS3Stack
from mediawiki_db_stack import MediaWikiDBStack
from mediawiki_asg_alb_stack import MediaWikiALBASGStack

app = cdk.App()

ami_map = {
    "af-south-1": "ami-028207f8881917f39",
    "ap-east-1": "ami-01e6c8f2ab310721c",
    "ap-northeast-1": "ami-0b75e38f5a56ada82",
    "ap-south-1": "ami-0c290bf29845f91ac",
    "ap-southeast-1": "ami-0292c68e0ac530398",
    "ca-central-1": "ami-0bf86d62e9d748e77",
    "eu-central-1": "ami-0b063c60b220a0574",
    "eu-north-1": "ami-04f4b2b9a871847f5",
    "eu-south-1": "ami-050662d936085be97",
    "eu-west-1": "ami-0c0e8c8bc308182d5",
    "me-south-1": "ami-0fe9f5648700507ff",
    "sa-east-1": "ami-03083fbcd9c410a1e",
    "us-east-1": "ami-05dc324761386f3a9",
    "us-west-1": "ami-04b5b5f4b328a8b16",
    "cn-north-1": "ami-0741e7b8b4fb0001c",
    "cn-northwest-1": "ami-0883e8062ff31f727",
    "us-gov-east-1": "ami-0fe6338c47e61cd5d",
    "us-gov-west-1": "ami-087ee83c8de303181",
    "ap-northeast-2": "ami-01119d2bc7609e870",
    "ap-southeast-2": "ami-08af7160732ddc242",
    "eu-west-2": "ami-033481a25f7e26aca",
    "us-east-2": "ami-04ea83ef6e494c1f2",
    "us-west-2": "ami-080471172a731411b",
    "ap-northeast-3": "ami-0345bcaead8878035",
    "eu-west-3": "ami-0953b38f670ad3e1e"
}

vpc_stack = VPCStack(app, "MediaWiki-VPC", region_name='mu', env_name='prod',
                     # If you don't specify 'env', this stack will be environment-agnostic.
                     # Account/Region-dependent features and context lookups will not work,
                     # but a single synthesized template can be deployed anywhere.

                     # Uncomment the next line to specialize this stack for the AWS Account
                     # and Region that are implied by the current CLI configuration.

                     env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                         region=os.getenv('CDK_DEFAULT_REGION')),

                     # Uncomment the next line if you know exactly what Account and Region you
                     # want to deploy the stack to. */

                     # env=core.Environment(account='123456789012', region='us-east-1'),

                     # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
                     )

deployments3 = DeploymentS3Stack(app, "MediaWiki-Deployment", env_name='prod', website_branch='main',
                                 # If you don't specify 'env', this stack will be environment-agnostic.
                                 # Account/Region-dependent features and context lookups will not work,
                                 # but a single synthesized template can be deployed anywhere.

                                 # Uncomment the next line to specialize this stack for the AWS Account
                                 # and Region that are implied by the current CLI configuration.

                                 env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                                     region=os.getenv('CDK_DEFAULT_REGION')),

                                 # Uncomment the next line if you know exactly what Account and Region you
                                 # want to deploy the stack to. */

                                 # env=core.Environment(account='123456789012', region='us-east-1'),

                                 # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
                                 )

iam_stack = IamStack(app, "MediaWiki-Iam", deployments3=deployments3.deploymnet_bucket,
                     # If you don't specify 'env', this stack will be environment-agnostic.
                     # Account/Region-dependent features and context lookups will not work,
                     # but a single synthesized template can be deployed anywhere.

                     # Uncomment the next line to specialize this stack for the AWS Account
                     # and Region that are implied by the current CLI configuration.

                     env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                         region=os.getenv('CDK_DEFAULT_REGION')),

                     # Uncomment the next line if you know exactly what Account and Region you
                     # want to deploy the stack to. */

                     # env=core.Environment(account='123456789012', region='us-east-1'),

                     # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
                     )

# mediawiki_stack = MediaWikiStack(app, "MediaWiki-App", region_name='mu', env_name='prod', vpc=vpc_stack.vpc,
#                                  role=iam_stack.app_role, ami_map=ami_map,
#                                  # If you don't specify 'env', this stack will be environment-agnostic.
#                                  # Account/Region-dependent features and context lookups will not work,
#                                  # but a single synthesized template can be deployed anywhere.
#
#                                  # Uncomment the next line to specialize this stack for the AWS Account
#                                  # and Region that are implied by the current CLI configuration.
#
#                                  env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
#                                                      region=os.getenv('CDK_DEFAULT_REGION')),
#
#                                  # Uncomment the next line if you know exactly what Account and Region you
#                                  # want to deploy the stack to. */
#
#                                  # env=core.Environment(account='123456789012', region='us-east-1'),
#
#                                  # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
#                                  )

mediawiki_alb_asg_stack = MediaWikiALBASGStack(app, "MediaWiki-Alb-asg", region_name='mu', env_name='prod',
                                               vpc=vpc_stack.vpc,
                                               role=iam_stack.app_role, ami_map=ami_map,
                                               # If you don't specify 'env', this stack will be environment-agnostic.
                                               # Account/Region-dependent features and context lookups will not work,
                                               # but a single synthesized template can be deployed anywhere.

                                               # Uncomment the next line to specialize this stack for the AWS Account
                                               # and Region that are implied by the current CLI configuration.

                                               env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                                                                   region=os.getenv('CDK_DEFAULT_REGION')),

                                               # Uncomment the next line if you know exactly what Account and Region you
                                               # want to deploy the stack to. */

                                               # env=core.Environment(account='123456789012', region='us-east-1'),

                                               # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
                                               )

# mediawiki_db_stack = MediaWikiDBStack(app, "MediaWiki-DB", region_name='mu', env_name='prod', vpc=vpc_stack.vpc,
#                                       role=iam_stack.app_role, app_system=mediawiki_stack.mediawiki_app_system,
#                                       ami_map=ami_map
#                                       # If you don't specify 'env', this stack will be environment-agnostic.
#                                       # Account/Region-dependent features and context lookups will not work,
#                                       # but a single synthesized template can be deployed anywhere.
#
#                                       # Uncomment the next line to specialize this stack for the AWS Account
#                                       # and Region that are implied by the current CLI configuration.
#
#                                       # env=core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
#
#                                       # Uncomment the next line if you know exactly what Account and Region you
#                                       # want to deploy the stack to. */
#
#                                       # env=core.Environment(account='123456789012', region='us-east-1'),
#
#                                       # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
#                                       )

app.synth()
