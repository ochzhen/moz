import os

import datetime

DEBUG = True
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SECRET_KEY = os.environ.get('MOZ_SECRET_KEY', 'SUPER_SECRET_KEY')

# MySQL connection settings
DB_NAME = 'sql11223417'
DB_USER = 'sql11223417'
DB_PASSWORD = os.environ.get('DB_PWD')
DB_HOST = 'sql11.freemysqlhosting.net'
DB_PORT = 3306

SECURITY_PASSWORD_SALT = datetime.datetime.now()

# mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# gmail authentication
MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']

# mail accounts
MAIL_DEFAULT_SENDER = 'moz.noreply@gmail.com'