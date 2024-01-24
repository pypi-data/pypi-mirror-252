===============
**aws_crawler**
===============

Overview
--------

Crawl through active AWS accounts in an organization using master assumed role.

Usage
-----

Installation:

.. code-block:: BASH

    pip3 install aws_crawler
    python3 -m pip install aws_crawler

Example:

.. code-block:: PYTHON

   """Get caller identity from the STS service."""
   import sys
   import boto3
   from botocore import exceptions
   import aws_crawler

   # Get arguments.
   access_key = sys.argv[1]
   secret_key = sys.argv[2]
   session_token = sys.argv[3]
   thread_num = 10
   role_name = 'AWSViewOnlyAccess'
   region_name = 'us-east-1'

   # Get account list.
   accounts = aws_crawler.list_accounts(
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
         credentials = aws_crawler.get_credentials(
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
