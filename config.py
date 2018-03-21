import os

DEBUG = True
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SECRET_KEY = os.environ.get('MOZ_SECRET_KEY', 'SUPER_SECRET_KEY')
SECURITY_PASSWORD_SALT = '16756d01a4bbbfa4800b3af15953ada021ec508e'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/moz/files'
DB_NAME = os.environ.get('DB_NAME', 'sql11223417')
DB_USER = os.environ.get('DB_USER', 'sql11223417')
DB_PASSWORD = os.environ.get('DB_PWD')
DB_HOST = os.environ.get('DB_HOST', 'sql11.freemysqlhosting.net')
DB_PORT = int(os.environ.get('DB_PORT', 3306))
ADMIN_PATH = '/admin'
DEFAULT_ADMIN_USER = os.environ.get('ADMIN_USER', 'admin@admin.com')
DEFAULT_ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')
MIN_PASSWORD_LENGTH = 8


# mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# gmail authentication
MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']

# mail accounts
MAIL_DEFAULT_SENDER = 'noreply.moz@gmail.com'
