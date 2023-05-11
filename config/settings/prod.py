from .base import *


SECRET_KEY = get_secret(
    secret_name='DJANGO_SECRET_KEY',
    region_name=os.getenv('REGION_NAME')
).get('DJANGO_SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['*']


# 아직 사용하지 않지만, AWS Secrets Manager에서 가져오는 코드 작성하기
secrets = get_secret(
    secret_name=secret_name,
    region_name=os.getenv('REGION_NAME'),
)

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': db_name,
    'USER': secrets.get('username'),
    'PASSWORD': secrets.get('password'),
    'HOST': hostname,
    'PORT': os.getenv('RDS_PORT'),
}
