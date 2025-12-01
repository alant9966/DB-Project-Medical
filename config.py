import os

MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'medical_app_user')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'aws.cs3083!user')
MYSQL_DB = os.environ.get('MYSQL_DB', 'medical_db')

MYSQL_CURSORCLASS = 'DictCursor'
SECRET_KEY = os.environ.get('SECRET_KEY', 'this-is-the-secret-key')