import boto3
import csv

region = "me-south-1"
ACCESS_KEY_ID = ""
SECRET_KEY_ID = ""
STS_TOKEN = ""

session = boto3.Session(aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_KEY_ID, aws_session_token=STS_TOKEN, region_name=region)
#session = boto3.Session(region_name="eu-west-1")
org_client = session.client('organizations')
sts_client = session.client('sts')

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
    

    print(awsaccount_list)
account_list()