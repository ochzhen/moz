from flask import Flask, render_template
from flask_login import LoginManager
from peewee import SqliteDatabase

app = Flask(__name__)

app.config.from_object('config')

login = LoginManager()
login.init_app(app)
login.login_view = 'auth.login'


@login.user_loader
def load_user(user_id):
    return User.select().where((User.id == int(user_id))).first()


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


db = SqliteDatabase('moz.db')
# db = MySQLDatabase(
#     app.config['DB_NAME'],
#     user=app.config['DB_USER'],
#     password=app.config['DB_PASSWORD'],
#     host=app.config['DB_HOST'],
#     port=int(app.config['DB_PORT'])
# )


from moz.auth.models import User

def create_tables():
    with db:
        db.create_tables([User])


from main.views import main as main_module
from auth.views import auth as auth_module

app.register_blueprint(main_module)
app.register_blueprint(auth_module)
