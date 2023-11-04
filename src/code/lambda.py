import json
import requests
import boto3

def main(event, context):
    secret_name = "rds/fastfood/secret"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(get_secret_value_response['SecretString'])
        # Use the secret data in your Lambda function
        username = secret['username']
        password = secret['password']        

        # Check if the event contains a body
        if 'body' in event:
            request_body = event['body']
            # You may need to parse the body as JSON if it's a JSON-encoded request
            # request_body = json.loads(request_body)

            response = {
                'statusCode': 200,
                'username': username
            }
        else:
            response = {
                'statusCode': 400,
                'body': 'No request body found'
            }

        return response
    except Exception as e:
        print("Error:", e)
        # Handle errors as needed