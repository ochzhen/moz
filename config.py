import os
import sys

DEBUG = True
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SECRET_KEY = os.environ.get('MOZ_SECRET_KEY', 'SUPER_SECRET_KEY')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/moz/files'
DB_NAME = 'sql11223417'
DB_USER = 'sql11223417'
DB_PASSWORD = os.environ.get('DB_PWD', 'xQPRI7R2Bl')
DB_HOST = 'sql11.freemysqlhosting.net'
DB_PORT = 3306
ADMIN_PATH = '/admin'
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
