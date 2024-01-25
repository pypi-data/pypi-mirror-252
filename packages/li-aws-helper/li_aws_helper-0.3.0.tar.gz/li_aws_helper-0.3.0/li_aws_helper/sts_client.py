import os
import boto3

from li_aws_helper.aws_config import AWSConfig


def refresh_token(token_code: str):
    aws_config = AWSConfig(load_config=True)

    session = boto3.session.Session(
        aws_access_key_id=aws_config.access_key,
        aws_secret_access_key=aws_config.secret_key
    )

    client = session.client(service_name='sts', region_name=aws_config.region_name)

    response = client.get_session_token(
        DurationSeconds=129600,
        SerialNumber=aws_config.mfa_arn,
        TokenCode=token_code)

    if response:
        credentials = response['Credentials']

        print(credentials["AccessKeyId"])
        print(credentials["SecretAccessKey"])

        items = ['[default]',
                 f'aws_secret_access_key = {credentials["SecretAccessKey"]}',
                 f'aws_access_key_id = {credentials["AccessKeyId"]}',
                 f'aws_session_token = {credentials["SessionToken"]}']

        user_aws_credentials_file = f"{os.path.expanduser('~')}/.aws/credentials"
        with open(user_aws_credentials_file, 'w+') as file:
            items = map(lambda x: x + '\n', items)
            file.writelines(items)



# refresh_token(xxxx)
