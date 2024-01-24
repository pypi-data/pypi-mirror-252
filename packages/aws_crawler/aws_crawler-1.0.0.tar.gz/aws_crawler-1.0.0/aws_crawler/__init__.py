#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Crawl through active AWS accounts in an organization using master assumed role."""
import sys
import boto3
from botocore import exceptions


__veersion__ = '1.0.0'


def list_accounts(
    access_key: str,
    secret_key: str,
    session_token: str,
    region_name: str
) -> list:
    """List all AWS accounts in the organization."""
    print("Getting accounts...")

    org = boto3.client(
        'organizations',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token,
        region_name=region_name
    )

    paginator = org.get_paginator('list_accounts')
    accounts = []
    for page in paginator.paginate():
        for account in page['Accounts']:
            if account['Status'] == 'ACTIVE':
                accounts.append(account)
    
    print(f"Found {len(accounts)} active accounts...")

    return accounts


def get_credentials(
    access_key: str,
    secret_key: str,
    session_token: str,
    region_name: str,
    role_arn: str
) -> dict:
    """Get AWS assume role credentials with STS."""
    sts = boto3.client(
        'sts',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token,
        region_name=region_name
    )

    sts_r = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName="aws-org-crawler"
    )

    return {
        'aws_access_key_id': sts_r["Credentials"]["AccessKeyId"],
        'aws_secret_access_key': sts_r["Credentials"]["SecretAccessKey"],
        'aws_session_token': sts_r["Credentials"]["SessionToken"],
        'region_name': region_name
    }


def main():
    """Execute test function."""
    # Get arguments.
    if len(sys.argv) < 4 or len(sys.argv) > 7:
        print(
            f'Usage: python {sys.argv[0]}'
            ' <access_key>'
            ' <secret_key>'
            ' <session_token>'
            ' [<thread_num: 10>'
            ' <role_name: AWSViewOnlyAccess>'
            ' <region_name: us-east-1>]'
        )
        sys.exit(1)

    access_key = sys.argv[1]
    secret_key = sys.argv[2]
    session_token = sys.argv[3]

    try:
        thread_num = int(sys.argv[4])
    except IndexError:
        thread_num = 10

    try:
        role_name = sys.argv[5]
    except IndexError:
        role_name = 'AWSViewOnlyAccess'

    try:
        region_name = sys.argv[6]
    except IndexError:
        region_name = 'us-east-1'

    # Get account list.
    accounts = list_accounts(
        access_key,
        secret_key,
        session_token,
        region_name
    )
    account_ids = [account['Id'] for account in accounts]

    # Crawl through each account.
    for account_id in account_ids:
        print(f"Working on {account_id}...")

        try:
            credentials = get_credentials(
                access_key,
                secret_key,
                session_token,
                region_name,
                f'arn:aws:iam::{account_id}:role/{role_name}'
            )

            client = boto3.client(
                'sts',
                aws_access_key_id=credentials['aws_access_key_id'],
                aws_secret_access_key=credentials['aws_secret_access_key'],
                aws_session_token=credentials['aws_session_token'],
                region_name=credentials['region_name']
            )

            response = client.get_caller_identity()['UserId']
        
        except exceptions.ClientError as e:
            response = 'Could not assume role'
        
        print(response)


if __name__ == '__main__':
    main()
