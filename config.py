import os

# MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
# MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
# MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
# MYSQL_DB = os.environ.get('MYSQL_DB', 'medical_db')

# MYSQL_CURSORCLASS = 'DictCursor'
# SECRET_KEY = os.environ.get('SECRET_KEY', 'this-is-the-secret-key')

MYSQL_DB = os.environ.get('MYSQL_HOST', 'medical_db')
MYSQL_HOST = os.environ.get('MYSQL_USER', 'medical-db.cryww6kq4mgk.us-east-2.rds.amazonaws.com')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'aws.cs3083!')
MYSQL_USER = os.environ.get('MYSQL_DB', 'admin')

MYSQL_CURSORCLASS = 'DictCursor'
SECRET_KEY = os.environ.get('SECRET_KEY', '61bcf92316b5becdb2e41359ae539b59d28cd7fb75598fd22e214099ad6e7db2')