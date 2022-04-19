import boto3

region="me-south-1"
awsaccount_list = ["855926410276"]


session = boto3.Session(region_name=region)
org_client = session.client('organizations')
sts_client = session.client('sts')


def describe_ec2():
    for aws_account in awsaccount_list:
        awsaccount = sts_client.assume_role(
            RoleArn=f'arn:aws:iam::{aws_account}:role/OrganizationAccountAccessRole',
            RoleSessionName='awsaccount_session'
        )
        ACCESS_KEY = awsaccount['Credentials']['AccessKeyId']
        SECRET_KEY = awsaccount['Credentials']['SecretAccessKey']
        SESSION_TOKEN = awsaccount['Credentials']['SessionToken']
        ec2_client = boto3.client('ec2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, aws_session_token=SESSION_TOKEN, region_name=region)
        resp =ec2_client.describe_instances()
        print(f"############  Instance List for Account {aws_account} ################################")
        for reservation in resp['Reservations']:
            for instance in reservation['Instances']:
                print("Running Instance Image ID: {} Running instance Instance Type: {} Running Instance Keyname {}".format(instance['InstanceId'],instance['InstanceType'],instance['KeyName']))


describe_ec2()