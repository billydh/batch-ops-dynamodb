import boto3
from botocore.exceptions import ClientError
import sys

client = boto3.client("dynamodb",
                      endpoint_url="http://localhost:8042")

demo_table_name = "demo-customer-info"


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
    customer_id = sys.argv[1]
    last_name = sys.argv[2]
    email_address = sys.argv[3]

    insert_dummy_record(demo_table_name, customer_id, last_name, email_address)

    print(f"Inserting record with customerId {customer_id}")
