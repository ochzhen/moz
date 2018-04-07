# coding=utf-8
import datetime
import os
import flask_admin as admin
from flask import Flask, render_template, request
from flask_babelex import Babel
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from peewee import DoesNotExist
from playhouse.pool import PooledMySQLDatabase

from auth.views import auth as auth_module
from config import ADMIN_PATH, DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_USER, DEBUG


app = Flask(__name__, static_folder='static')
babel = Babel(app)
app.config.from_object('config')

import logging
from logging.handlers import RotatingFileHandler

if not os.path.exists(app.config['LOGGING_FOLDER']):
    os.makedirs(app.config['LOGGING_FOLDER'])

logging_location = os.path.join(app.config['LOGGING_FOLDER'], app.config['LOGGING_FILENAME'])

file_handler = RotatingFileHandler(logging_location, maxBytes=1000000, backupCount=1)
file_handler.setLevel(app.config['LOGGING_LEVEL'])
file_formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
file_handler.setFormatter(file_formatter)
app.logger.setLevel(app.config['LOGGING_LEVEL'])
app.logger.addHandler(file_handler)

login = LoginManager()
login.session_protection = 'strong'
login.init_app(app)
login.login_view = 'auth.login'
login.login_message = u'Будь ласка, увійдіть у систему.'
login.login_message_category = 'info'

mail = Mail(app)


@babel.localeselector
def get_locale():
    return 'uk'


@login.user_loader
def load_user(user_id):
    return User.select().where((User.id == int(user_id))).first()


@app.errorhandler(404)
def not_found(error):
    app.logger.warning('Page not found: %s', (request.path))
    return render_template('404.html')


@app.errorhandler(500)
def server_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('500.html')


@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Unhandled Exception: %s', (e))
    return render_template('500.html')


@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "deny"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
    response.headers["Referrer-Policy"] = "origin"
    return response


# db = SqliteDatabase(os.path.join(BASE_DIR, 'moz.db'))

db = PooledMySQLDatabase(
    app.config['DB_NAME'],
    user=app.config['DB_USER'],
    password=app.config['DB_PASSWORD'],
    host=app.config['DB_HOST'],
    port=int(app.config['DB_PORT']),
    max_connections=7,
    stale_timeout=1000
)

from moz.auth.models import User
from main.models import MOZDocument, Category
from main.admin import MOZDocumentAdmin, CategoryAdmin, ProtectedIndex, UserAdmin


def create_tables():
    with db:
        db.create_tables([User, MOZDocument, Category])


def create_admin_user():
    try:
        User.get(User.email == DEFAULT_ADMIN_USER)
        return
    except DoesNotExist:
        pass

    user = User(email=DEFAULT_ADMIN_USER,
                active=True,
                is_admin=True,
                registered_at=datetime.datetime.now(),
                speciality='Admin',
                occupation='Admin',
                confirmed_at=datetime.datetime.now()
                )
    user.set_password(DEFAULT_ADMIN_PASSWORD)
    user.save()


from main.views import main as main_module

app.register_blueprint(main_module)
app.register_blueprint(auth_module)

adm = admin.Admin(app, template_mode='bootstrap3', name='moz', url=ADMIN_PATH,
                  index_view=ProtectedIndex())
adm.add_view(UserAdmin(User, name=u'Користувачі'))
adm.add_view(CategoryAdmin(Category, name=u'Категорії'))
adm.add_view(MOZDocumentAdmin(MOZDocument, name=u'Документи МОЗ'))
csrf = CSRFProtect(app)

