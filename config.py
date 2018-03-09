import os
import sys

DEBUG = True
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SECRET_KEY = os.environ.get('MOZ_SECRET_KEY', 'SUPER_SECRET_KEY')

DB_NAME = 'sql11223417'
DB_USER = 'sql11223417'
DB_PASSWORD = os.environ.get('DB_PWD')
DB_HOST = 'sql11.freemysqlhosting.net'
DB_PORT = '3306'

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))