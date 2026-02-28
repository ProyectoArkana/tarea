import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    ENV = os.getenv('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS=True