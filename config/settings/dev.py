# from dotenv import load_dotenv
from .base import *

# load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True   # False for prod.py
ALLOWED_HOSTS = ['*']