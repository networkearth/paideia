from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    Stack
)

from constructs import Construct

class UserStack(Stack):
    def __init__(self, scope: Construct, id: str, conf: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        user_name = '-'.join([conf['stage'], conf['name']])
        user = iam.User(
            self, user_name, user_name=user_name
        )

        group = iam.Group(
            self, user_name + "s", group_name=user_name + "s"
        )

        user.add_to_group(group)

        bucket_name = 'paideia-dev-dvc'
        bucket = s3.Bucket.from_bucket_name(
            self, bucket_name, bucket_name=bucket_name
        )
        bucket.grant_read_write(group)
