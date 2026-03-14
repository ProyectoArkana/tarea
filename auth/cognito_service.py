import boto3
import os
import hmac
import hashlib
import base64

client = boto3.client(
    "cognito-idp",
    region_name=os.environ.get("AWS_REGION")
)

USER_POOL_ID = os.environ.get("USER_POOL_ID")
# Necesitarás el Client ID de tu aplicación en Cognito para el Login
CLIENT_ID = os.environ.get("COGNITO_CLIENT_ID") 
# Se agrega el Secret Key para calcular el hash
CLIENT_SECRET = os.environ.get("COGNITO_CLIENT_SECRET")

def get_secret_hash(username):
    """Calcula el SECRET_HASH requerido por Cognito cuando el App Client tiene un Secret"""
    msg = username + CLIENT_ID
    dig = hmac.new(
        str(CLIENT_SECRET).encode('utf-8'),
        msg.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()

def create_cognito_user(email:str, password:str):
    response = client.admin_create_user(
        UserPoolId=USER_POOL_ID,
        Username=email,
        UserAttributes=[
            {"Name": "email","Value": email},
            {"Name": "email_verified","Value": "true"}
        ],
        MessageAction="SUPPRESS" 
    )

    client.admin_set_user_password(
        UserPoolId=USER_POOL_ID,
        Username=email,
        Password=password,
        Permanent=True
    )

    attributes= response ["User"]["Attributes"]

    sub = next (
        attr["Value"] for attr in attributes if attr["Name"] == "sub"
    )

    return sub

# --- NUEVAS FUNCIONES PARA MFA ---

def login_cognito(email, password):
    """Inicia sesión y detecta si se requiere configuración de MFA"""
    auth_params = {
        'USERNAME': email,
        'PASSWORD': password
    }
    
    # Si existe el Secret en el .env, calculamos e incluimos el hash
    if CLIENT_SECRET:
        auth_params['SECRET_HASH'] = get_secret_hash(email)

    return client.admin_initiate_auth(
        UserPoolId=USER_POOL_ID,
        ClientId=CLIENT_ID,
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters=auth_params
    )

def associate_mfa_token(session):
    """Solicita el SecretCode a Cognito para generar el QR en el frontend"""
    return client.associate_software_token(
        Session=session
    )

def verify_mfa_setup(session, user_code):
    """Confirma el primer código de la App para activar el MFA definitivamente"""
    return client.verify_software_token(
        Session=session,
        UserCode=user_code,
        FriendlyDeviceName='DispositivoUsuario'
    )