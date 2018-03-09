from peewee import Model, TextField, BooleanField, DateTimeField, CharField, ForeignKeyField
from moz import db

class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    email = TextField()
    password = TextField()
    active = BooleanField(default=True)
    confirmed_at = DateTimeField(null=True)


class Role(BaseModel):
    name = CharField(unique=True)
    description = TextField(null=True)


class UserRoles(BaseModel):
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)
