from datetime import datetime
from peewee import Model, TextField, BooleanField, DateTimeField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from moz import db


class BaseModel(Model):
    class Meta:
        database = db


class User(UserMixin, BaseModel):
    email = TextField()
    password = TextField()
    active = BooleanField(default=True)
    confirmed_at = DateTimeField(null=True)
    registered_at = DateTimeField(default=datetime.now)
    first_name = TextField()
    last_name = TextField()
    speciality = TextField()
    occupation = TextField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
