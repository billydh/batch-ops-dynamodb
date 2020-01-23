import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.types import TypeDeserializer

client = boto3.client("dynamodb",
                      endpoint_url="http://localhost:8042")

deserializer = TypeDeserializer()

demo_table_name = "demo-customer-info"

filter_expression = "begins_with(#emailAddress, :emailBeginsWith) AND " \
                    "begins_with(#lastName, :lastNameBeginsWith)"

expression_attribute_names = {
    "#emailAddress": "emailAddress",
    "#lastName": "lastName"
}

expression_attribute_values = {
    ":emailBeginsWith": {"S": "testing"},
    ":lastNameBeginsWith": {"S": "TEST"}
}


def get_customer_id_to_delete(table_name, filter_expr, expr_attr_names, expr_attr_values):
    try:
        response = client.scan(
            TableName=table_name,
            ProjectionExpression="customerId",
            Select="SPECIFIC_ATTRIBUTES",
            FilterExpression=filter_expr,
            ExpressionAttributeNames=expr_attr_names,
            ExpressionAttributeValues=expr_attr_values
        )

        # customer_ids = [[deserializer.deserialize(v) for k, v in item.items()][0] for item in response.get("Items")]
    except ClientError as err:
        print(err)
    else:
        print(response)
        return response
        # print(customer_ids)
        # return customer_ids


def delete_record_by_customer_id(table_name, customer_id):
    try:
        response = client.delete_item(
            TableName=table_name,
            Key={
                "customerId": {"S": f"{customer_id}"}
            }
        )
    except ClientError as err:
        print(err)
    else:
        return response


if __name__ == "__main__":
    print("Getting customer ids to delete")
    print("============")

    id_list = get_customer_id_to_delete(demo_table_name,
                                        filter_expression,
                                        expression_attribute_names,
                                        expression_attribute_values)

    # for i in id_list:
    #     delete_record_by_customer_id(demo_table_name, i)
    #
    #     print(f"Deleting customer {i}")
