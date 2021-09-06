from aws_cdk import core as cdk
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3


class IamStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, deployments3: s3.Bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        ssm_actions = ["ssm:DescribeDocument",
                       "ec2messages:GetEndpoint",
                       "ec2messages:GetMessages",
                       "ssmmessages:OpenControlChannel",
                       "ssm:PutConfigurePackageResult",
                       "ssm:ListInstanceAssociations",
                       "ssm:GetParameter",
                       "ssm:UpdateAssociationStatus",
                       "ssm:GetManifest",
                       "ec2messages:DeleteMessage",
                       "ssm:UpdateInstanceInformation",
                       "ec2messages:FailMessage",
                       "ssmmessages:OpenDataChannel",
                       "ssm:GetDocument",
                       "ssm:PutComplianceItems",
                       "ssm:DescribeAssociation",
                       "ssm:GetDeployablePatchSnapshotForInstance",
                       "ec2messages:AcknowledgeMessage",
                       "ssm:GetParameters",
                       "ssmmessages:CreateControlChannel",
                       "ssmmessages:CreateDataChannel",
                       "ssm:PutInventory",
                       "ec2messages:SendReply",
                       "ssm:ListAssociations",
                       "ssm:UpdateInstanceAssociationStatus"]

        # self.ansible_role = iam.Role(self, id='default-ssm-role',
        #                              assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'),
        #                              managed_policies=[
        #                                  iam.ManagedPolicy.from_aws_managed_policy_name(
        #                                      managed_policy_name='AmazonEC2FullAccess'),
        #                                  iam.ManagedPolicy.from_aws_managed_policy_name(
        #                                      managed_policy_name='CloudWatchAgentServerPolicy')])
        #
        # self.ansible_role.add_to_policy(iam.PolicyStatement(actions=ssm_actions,
        #                                                     resources=['*']))

        self.app_role = iam.Role(self, id='default-app-role',
                                 assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'),
                                 managed_policies=[
                                     iam.ManagedPolicy.from_aws_managed_policy_name(
                                         managed_policy_name='CloudWatchAgentServerPolicy')
                                 ])
        self.app_role.add_to_policy(iam.PolicyStatement(actions=ssm_actions,
                                                        resources=['*']))

        self.app_role.add_to_policy(iam.PolicyStatement(actions=["s3:Put*",
                                                                 "s3:Get*",
                                                                 "s3:List*"],
                                                        resources=[deployments3.bucket_arn,
                                                                   deployments3.bucket_arn + '/*']))
