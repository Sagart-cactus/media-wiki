from aws_cdk import core as cdk
from aws_cdk import aws_s3 as s3


class DeploymentS3Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, env_name: str, website_branch: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.deploymnet_bucket = s3.Bucket(self, 'ansible_deployment' + env_name, versioned=True,
                                           bucket_name='ansible-deployment-' + env_name,
                                           removal_policy=cdk.RemovalPolicy.DESTROY)
