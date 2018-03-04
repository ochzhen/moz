from flask import Flask, render_template
from peewee import MySQLDatabase


app = Flask(__name__)

app.config.from_object('config')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


db = MySQLDatabase(
    app.config['DB_NAME'],
    user = app.config['DB_USER'],
    password = app.config['DB_PASSWORD'],
    host = app.config['DB_HOST'],
    port = app.config['DB_PORT']
)

from app.main.models import User, Role, UserRoles

def create_tables():
    with db:
        db.create_tables([User, Role, UserRoles])


from app.main.controllers import main as main_module
app.register_blueprint(main_module)


# create_tables()
