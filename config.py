import os
from dotenv import load_dotenv
from settings.secret import get_db_password

load_dotenv()


class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    ENV = os.getenv('FLASK_ENV')

    # Datos no sensibles desde .env
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    # Contraseña desde AWS Secrets Manager
    DB_PASSWORD = get_db_password()

    # Construcción dinámica de la URI
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = True