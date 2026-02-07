import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-12345'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+mysqlconnector://root:@localhost/kosan'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
