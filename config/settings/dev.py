import os

from dotenv import load_dotenv
from .base import *

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True   # False for prod.py
ALLOWED_HOSTS = []

# mysql database
# https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-rds.html
if 'RDS_HOSTNAME' in os.environ:
    DATABASES['users'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('RDS_DB_NAME'),
        'USER': os.getenv('RDS_USERNAME'),
        'PASSWORD': os.getenv('RDS_PASSWORD'),
        'HOST': os.getenv('RDS_HOSTNAME'),
        'PORT': os.getenv('RDS_PORT'),
    }
