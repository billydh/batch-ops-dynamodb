import boto3
from botocore.exceptions import ClientError
import random

client = boto3.client("dynamodb",
                      endpoint_url="http://localhost:8042")

demo_table_name = "demo-customer-info"
last_name_prefix = "TEST"
email_address_prefix = "testing"
email_address_domain = "@dummy.com"


def insert_dummy_record(table_name, customer_id, l_name, email):
    try:
        response = client.put_item(
            TableName=table_name,
            Item={
                "customerId": {"S": f"{customer_id}"},
                "lastName": {"S": f"{l_name}"},
                "emailAddress": {"S": f"{email}"}
            }
        )
    except ClientError as err:
        print(err)
    else:
        return response


if __name__ == "__main__":

    for i in range(10):
        random_no = random.randint(100, 900)
        last_name = last_name_prefix + str(random_no)
        email_address = email_address_prefix + str(random_no) + email_address_domain

        insert_dummy_record(demo_table_name, str(random_no), last_name, email_address)

        print(f"Inserting record number {i + 1} with customerId {random_no}")
