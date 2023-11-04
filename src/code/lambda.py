import json
import psycopg2
import boto3
import os

def main(event, context):
    try:        
        # Create a Secrets Manager client
        print("chegou")
        secret_name = "rds/fastfood/secret"
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name='us-east-1'
        )
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(get_secret_value_response['SecretString'])
        username = secret['username']
        password = secret['password']
        print('username: ' + username)

        #DB connection
        db_host = os.environ['RDS_ENDPOINT']
        db_name = os.environ['DB_NAME']
        print("DB NAME: "+os.environ.get('DB_NAME'))

        connection = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=username,
            password=password
        )
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