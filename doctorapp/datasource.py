import os
import boto3


# Name of the dynamodb table to inspect
database_name = os.environ.get("SECRET_DBNAME", "devops-challenge")
# Key column of the table to match against
lookup_keyname = os.environ.get("LOOKUP_KEYNAME", "code_name")
# Value to match against $lookup_keyname
lookup_keyvalue = os.environ.get("LOOKUP_KEYVALUE", "thedoctor")
# Column of the matched row to retrieve
secret_keyname = os.environ.get("SECRET_KEYNAME", "secret_code")


table = boto3.Session() \
    .resource("dynamodb") \
    .Table(database_name)


def get_secret():
    """
    Query a dynamodb table for a row matching our codename. Return the secret value.
    :return: str
    """
    result = table.query(
        KeyConditions={lookup_keyname: {
            'AttributeValueList': [lookup_keyvalue],
            'ComparisonOperator': 'EQ'}},
        AttributesToGet=[secret_keyname],
        Limit=1)

    if result["Items"]:
        item = result["Items"].pop()

        return item[secret_keyname]
