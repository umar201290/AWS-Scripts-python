import boto3
import csv

region="me-south-1"
# awsaccount_list = [""]
ACCESS_KEY_ID = ""
SECRET_KEY_ID = ""
STS_TOKEN = ""

session = boto3.Session(aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_KEY_ID, aws_session_token=STS_TOKEN, region_name=region)
# session = boto3.Session(region_name=region)
org_client = session.client('organizations')
sts_client = session.client('sts')
filename = ("rds_snapshots_list.csv")
fieldnames = ['AccountID','AccountName','Region','Snapshot Name', 'SnapShot Time']

def account_list():
    paginator = org_client.get_paginator('list_accounts')
    page_iterator = paginator.paginate()
    awsaccount = []
    account_id_list = []
    account_name_list = []
    for page in page_iterator:       
        for x in page['Accounts']:
            if (x['Status'] not in 'ACTIVE'):
                print('WARN: skipping non active account ', x['Id'], x['Name'], x['Status'])
                continue
                
            if (x['Id'] not in 'xxx') and (x['Id'] not in 'xxx'):
                account_id_list.append(x.get('Id'))
                account_name_list.append(x.get('Name'))
    
    awsaccount = [account_id_list, account_name_list]
    awsaccount_list = []
    xrange=range
    for i in xrange(len(awsaccount)):
        if i % 2 == 0:
            accountid = awsaccount[i]
            accountname = awsaccount[i + 1]
            for n in xrange(len(accountid)):
                awsaccount_list.append([accountid[n],accountname[n]])

    describe_rds_snapshots(awsaccount_list)

def describe_rds_snapshots(awsaccount_list):
    with open(filename, 'w', newline='') as csvFile:
        w = csv.writer(csvFile, dialect='excel')
        w.writerow(fieldnames)
        for aws_account in awsaccount_list:
            awsaccount = sts_client.assume_role(
                RoleArn=f'arn:aws:iam::{aws_account[0]}:role/OrganizationAccountAccessRole',
                RoleSessionName='awsaccount_session'
            )
            ACCESS_KEY = awsaccount['Credentials']['AccessKeyId']
            SECRET_KEY = awsaccount['Credentials']['SecretAccessKey']
            SESSION_TOKEN = awsaccount['Credentials']['SessionToken']
            EXPO_AWS_REGIONS = ["me-south-1","ap-south-1","eu-west-1"]

            for region in EXPO_AWS_REGIONS:
                print(f"Crawling in Account {aws_account[0]} in Region {region}, Please wait for final output :) U|\/|AR #####")
                rds_client = boto3.client('rds', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, aws_session_token=SESSION_TOKEN, region_name=region)
                db_snapshots =rds_client.describe_db_snapshots()
                for each in db_snapshots['DBSnapshots']:
                    Snapshot_name=each['DBSnapshotIdentifier']
                    Snapshot_time=each['SnapshotCreateTime']
                    # print(f"Snapshot name is {each['DBSnapshotIdentifier']} and creation time is {each['SnapshotCreateTime']} ")
                    raw = [
                            aws_account[0],
                            aws_account[1],
                            region,
                            Snapshot_name,
                            Snapshot_time
                        ]
                    w.writerow(raw)
                    raw = []
                cluster_snapshots = rds_client.describe_db_cluster_snapshots()
                for each in cluster_snapshots['DBClusterSnapshots']:
                    Snapshot_name=each['DBClusterSnapshotIdentifier']
                    Snapshot_time=each['SnapshotCreateTime']
                    # print(f"Snapshot name is {each['DBClusterSnapshotIdentifier']} and creation time is {each['SnapshotCreateTime']} ")
                    raw = [
                            aws_account[0],
                            aws_account[1],
                            region,
                            Snapshot_name,
                            Snapshot_time
                        ]
                    w.writerow(raw)
                    raw = []
    csvFile.close()

account_list()