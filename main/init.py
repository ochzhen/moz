from peewee import MySQLDatabase

from main.views import main as main_module
import flask_admin as admin
from config import ADMIN_PATH, DB_NAME, DB_HOST, DB_USER, DB_PORT, DB_PASSWORD

DB = MySQLDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)


def init_app(app):
    app.config.from_object('config')

    app.register_blueprint(main_module)
    from main.admin import MOZDocumentAdmin
    from main.models import MOZDocument
    adm = admin.Admin(app, template_mode='bootstrap3', name='moz', url=ADMIN_PATH)
    adm.add_view(MOZDocumentAdmin(MOZDocument))
    # create_tables(DB)
    return app


def create_tables(db):
    from main.models import User, Role, UserRoles, MOZDocument
    with db:
        db.create_tables([User, Role, UserRoles, MOZDocument])
