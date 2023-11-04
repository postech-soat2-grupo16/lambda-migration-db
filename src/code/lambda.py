import json
import psycopg2
import boto3
import os

def main(event, context):

    # Create a Secrets Manager client
    secret_name = "rds/fastfood/secret"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(get_secret_value_response['SecretString'])
        username = secret['username']
        password = secret['password']

        #DB connection
        db_params = {
            'host': os.environ.get('RDS_ENDPOINT', 'default_value'),
            'dbname': os.environ.get('DB_NAME'),
            'user': username,
            'password': password
        }
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        print("Connected to the database")

    except Exception as error:
        print("Error connecting to the database:", error)
        response = {
            'statusCode': 500,
            'msg': 'Error'
        }
        return response

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Database connection closed")            
            #Response        
            response = {
                'statusCode': 200,
                'username': username
            }
            return response