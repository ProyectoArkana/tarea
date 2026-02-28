import boto3
import json

def get_db_password():
    client = boto3.client("secretsmanager", region_name="us-east-2")
    
    response = client.get_secret_value(
        SecretId="api82/db/password"
    )
    
    secret = json.loads(response["SecretString"])
    return secret["DB_PASSWORD"]