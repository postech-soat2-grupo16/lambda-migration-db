import json
import psycopg2
import boto3
import os

def main(event, context):
    if 'body' in event:
        try:
            print("CHegou aqui")
            #Get data from body
            request_body = json.loads(event['body'])
            db_domain = request_body['db_domain']
            secret_name = request_body['secret']
            file_name = request_body['file_name']

            #Get query from S3 file
            query = get_query(db_domain, file_name).split(';')
            
            #Get secrets
            secret = get_secrets(secret_name)
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
                if len(q) > 0 or (q and q.strip()):
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
            print("Error connecting to the database: ", error)
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

def get_secrets(secret_name):
    # Create a Secrets Manager client
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name='us-east-1'
        )
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(get_secret_value_response['SecretString'])    
        return secret
    except Exception as e:
        print('Error SM ', e)

def get_query(db_domain, file_name):
    try:
        s3 = boto3.client('s3')
        bucket_name = os.environ['BUCKET_NAME']
        key = 'scripts/'+db_domain+'/'+file_name+'.sql'
        file = s3.get_object(Bucket=bucket_name, Key=key)
        query = file['Body'].read().decode('utf-8')
        return query
    except Exception as e:
        print('Error S3 ', e)
    