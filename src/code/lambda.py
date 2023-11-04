import json
import psycopg2
import boto3
import os

def main(event, context):
    try:        
        # Create a Secrets Manager client
        secret_name = "rds/fastfood/secret"
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name='us-east-1'
        )
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(get_secret_value_response['SecretString'])
        db_username = secret['username']
        db_password = secret['password']
        db_name = secret['dbname']
        db_host = secret['host']

        #DB conn

        connection = psycopg2.connect(
            host=db_host,
            dbname=db_name,
            user=db_username,
            password=db_password
        )
        cursor = connection.cursor()
        print("Connected to the database")
        
        cursor.close()
        connection.close()
        print("Database connection closed") 

        #Response        
        response = {
            'statusCode': 200,
            'username': username
        }
        return response
    except Exception as error:
        print("Error connecting to the database:", error)
        response = {
            'statusCode': 500,
            'msg': 'Error'
        }
        return response