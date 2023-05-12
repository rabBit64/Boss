"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

from dotenv import load_dotenv

load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'accounts',
    'boss',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'accounts.User'


# AWS Secrets Manager 시작
import boto3, json
from botocore.exceptions import ClientError


def get_secret(secret_name, region_name) -> dict:
    """
    권한이 있어야 접근할 수 있다. credential이라던가, EC2 인스턴스의 경우 IAM Role
    그럼 만약 secrets manager 접근 권한은 있는데, RDS 접근 권한이 없다면?
    비밀번호는 가져올 수 있다. 이번에는 아래 print문이 한번만 실행된다.
    
    shell_plus 실행시에도 실행된다.
    하지만 여전히 RDS로 접속은 불가능하다.
    users DB로 레코드 생성 어떻게하지? → .objects.using('users').create(...)
    두 권한 모두 있어야 된다.

    코드 출처는 만들 때  볼 수  있다.
    """
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    
    # Your code goes here.
    return json.loads(secret)

# AWS Secrets Manager 끝


# AWS Parameter Store 시작
if 'REGION_NAME' in os.environ:
    '''
    필요한 환경 변수와 충분한 권한이 있는 경우 mysql 접속을 시도하도록 수정
    '''
    # AWS SSM 클라이언트 인스턴스 생성
    ssm_client = boto3.client("ssm", region_name=os.getenv('REGION_NAME'))

    # Parameter Store에 저장되어 있는 변수 가져오기
    try:
        secret_name = ssm_client.get_parameter(Name='/bossmarket/rds/secret_name', WithDecryption=True).get('Parameter').get('Value')
        hostname = ssm_client.get_parameter(Name='/bossmarket/rds/hostname', WithDecryption=True).get('Parameter').get('Value')
        db_name = ssm_client.get_parameter(Name='/bossmarket/rds/db_name', WithDecryption=True).get('Parameter').get('Value')


        # Use this code snippet in your app.
        # If you need more information about configurations
        # or implementing the sample code, visit the AWS docs:
        # https://aws.amazon.com/developer/language/python/

        # mysql database
        # https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-rds.html
        if 'RDS_PORT' in os.environ and 'REGION_NAME' in os.environ:
            try:
                secrets = get_secret(
                    secret_name=secret_name,
                    region_name=os.getenv('REGION_NAME'),
                    # region_name='ap-northeast-2',
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
                    'PORT': os.getenv('RDS_PORT'),
                    # 'PORT': '3306',
                }
            except ClientError as e:
                print("에러 내용(Secrets Manager) :", e.response)

    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDeniedException':
            print("Parameter Store로 접근이 거부되었습니다.")
        else:
            print("에러 내용(Parameter Store) :", e.response)

# AWS Parameter Store 끝