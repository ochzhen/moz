from peewee import Model, TextField, BooleanField, DateTimeField, CharField, ForeignKeyField
from moz import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class BaseModel(Model):
    class Meta:
        database = db


class User(UserMixin, BaseModel):
    email = TextField()
    password = TextField()
    active = BooleanField(default=True)
    confirmed_at = DateTimeField(null=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Role(BaseModel):
    name = CharField(unique=True)
    description = TextField(null=True)


class UserRoles(BaseModel):
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)