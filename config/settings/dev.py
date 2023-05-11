# from dotenv import load_dotenv
from .base import *

# load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True   # False for prod.py
ALLOWED_HOSTS = ['*']


# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/


# mysql database
# https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-rds.html
if 'RDS_PORT' in os.environ:
    secrets = get_secret(
        secret_name=secret_name,
        # region_name=os.getenv('REGION_NAME'),
        region_name='ap-northeast-2',
    )
    '''
    Model Manager를 'users' DB를 사용하도록 일일이 커스텀 할 수 없어서
    RDS 관련 정보가 환경변수에 있는 경우 MySQL을 디폴트 DB로 사용하도록 수정
    '''
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': db_name,
        'USER': secrets.get('username'),
        'PASSWORD': secrets.get('password'),
        'HOST': hostname,
        # 'PORT': os.getenv('RDS_PORT'),
        'PORT': '3306',
    }
    # print(DATABASES['default']['PASSWORD'])