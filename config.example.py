# Database Configuration
#
# SECURITY BEST PRACTICE:
# - Do NOT use 'root' user for your application
# - Use the dedicated 'medical_app_user' created in SECURITY_ROLES_PERMISSIONS.sql
# - Store sensitive passwords in environment variables, not in code

import os

# Use environment variables for sensitive data (recommended)
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'medical_app_user')  # Changed from 'root'
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'secure_app_password_2025')  # Use strong password
MYSQL_DB = os.environ.get('MYSQL_DB', 'medical_db')

MYSQL_CURSORCLASS = 'DictCursor'

# IMPORTANT: Change this to a random secret key in production
# Generate with: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY = os.environ.get('SECRET_KEY', 'this-is-the-secret-key')
