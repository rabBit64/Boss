import os

from dotenv import load_dotenv
from .base import *

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = False   # False for prod.py
ALLOWED_HOSTS = []


# 아직 사용하지 않지만, AWS Secrets Manager에서 가져오는 코드 작성하기
DATABASES['users'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': os.getenv('RDS_DB_NAME'),
    'USER': os.getenv('RDS_USERNAME'),
    'PASSWORD': os.getenv('RDS_PASSWORD'),
    'HOST': os.getenv('RDS_HOSTNAME'),
    'PORT': os.getenv('RDS_PORT'),
}
