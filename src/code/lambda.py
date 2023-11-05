import json
import psycopg2
import boto3
import os

def main(event, context):
    if 'body' in event:
        try:
            #Get query from S3 file
            request_body = json.loads(event['body'])
            table = request_body['table']
            query = get_query(table).split(';')
            
            #Get secrets
            secret = get_secrets()
            db_username = secret['username']
            db_password = secret['password']
            db_name = secret['dbname']
            db_host = secret['host']
            db_port = secret['port']

            #DB connection
            connection = psycopg2.connect(
                host=db_host,
                dbname=db_name,
                user=db_username,
                password=db_password,
                port=db_port
            )
            cursor = connection.cursor()
            print("Connected to the database")
            
            #Executa script
            for index, q in enumerate(query):
                if len(q) > 0:
                    print(f"Iteração {index + 1}: {q}")
                    cursor.execute(q)
                    connection.commit()
                else:
                    print("FIM")

            cursor.close()
            connection.close()
            print("Database connection closed") 

            #Response        
            response = {
                'statusCode': 200,
                 'headers': {
                    "Content-Type": "application/json"
                },
                'body': json.dumps({
                    'msg': 'Script OK'
                })
            }
            return response
        except Exception as error:
            print("Error connecting to the database:", error)
            response = {
                'statusCode': 500,
                 'headers': {
                    "Content-Type": "application/json"
                },
                'body': json.dumps({
                    'msg': 'error'
                })
            }
            return response
    else:
        return {
            'statusCode': 400,
                'headers': {
                "Content-Type": "application/json"
            },
            'body': json.dumps({
                'msg': 'No request Body'
            })
        }

def get_secrets():
    # Create a Secrets Manager client
    secret_name = "rds/fastfood/secret"
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(get_secret_value_response['SecretString'])    
    return secret

def get_query(table):
    try:
        s3 = boto3.client('s3')
        bucket_name = os.environ['BUCKET_NAME']
        key = 'scripts/'+table+'.sql'
        file = s3.get_object(Bucket=bucket_name, Key=key)
        query = file['Body'].read().decode('utf-8')
        return query
    except Exception as e:
        print('Error S3', e)
    