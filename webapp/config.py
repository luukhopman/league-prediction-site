import os
from datetime import datetime

if os.environ.get('DATABASE_URL'):  # Heroku
    DEV = False
else:
    DEV = True


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    API_KEY = os.environ.get('FOOTBALL_DATA_API_KEY')
    ADMIN_PIN = os.environ.get('ADMIN_PIN', '1111')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    if DEV:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///User.db'
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    if datetime.today().month != 8:
        ACTIVE_SEASON = True
    else:
        ACTIVE_SEASON = False
