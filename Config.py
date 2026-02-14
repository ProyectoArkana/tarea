import os
from dotenv import load_dotenv

env = os.getenv('FLASK_ENV', 'development')

if env == 'production':
    load_dotenv('.env.production')
else:
    load_dotenv('.env.development')

class Config:
    ENV = env
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
