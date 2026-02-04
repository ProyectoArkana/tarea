import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    ENV = os.getenv('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS=True