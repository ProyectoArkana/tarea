import boto3
import json
from botocore.exceptions import ClientError


class SecretsManagerService:

    def __init__(self, region: str, secret_name: str):
        self.region = region
        self.secret_name = secret_name
        self.client = boto3.client(
            "secretsmanager",
            region_name=self.region
        )

    def get_db_password(self) -> str:
        try:
            response = self.client.get_secret_value(
                SecretId=self.secret_name
            )

            secret = json.loads(response["SecretString"])
            return secret["DB_PASSWORD"]

        except ClientError as e:
            raise e

    def set_db_password(self, new_password: str) -> None:
        secret_value = json.dumps({
            "DB_PASSWORD": new_password
        })

        try:
            self.client.update_secret(
                SecretId=self.secret_name,
                SecretString=secret_value
            )
            print("Secreto actualizado correctamente.")

        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                self.client.create_secret(
                    Name=self.secret_name,
                    SecretString=secret_value
                )
                print("Secreto creado correctamente.")
            else:
                raise e