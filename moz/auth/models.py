# coding=utf-8
from datetime import datetime
from peewee import Model, TextField, BooleanField, DateTimeField
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from peewee import Model, BooleanField, DateTimeField, CharField, AutoField
from peewee import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from config import MIN_PASSWORD_LENGTH
from moz import db


class BaseModel(Model):
    class Meta:
        database = db


class User(UserMixin, BaseModel):
    id = AutoField(null=False, index=True, unique=True, primary_key=True)
    email = CharField(unique=True, index=True, null=False, max_length=254, verbose_name=u'Електрона пошта',
                      help_text=u'Це поле є унікальнім')
    first_name = CharField(max_length=64, null=False, verbose_name=u'Ім\'я')
    last_name = CharField(max_length=64, null=False, verbose_name=u'Прізвище')
    speciality = CharField(max_length=128, null=False, verbose_name=u'Спеціальність')
    occupation = CharField(max_length=128, null=False, verbose_name=u'Місце роботи')
    password = CharField(null=False, max_length=256, verbose_name=u'Пароль',
                         help_text=u'Пароль зебрігаєтся у шифрованому виді')
    active = BooleanField(null=False, default=False, verbose_name=u'Користувач пітверджений')
    is_admin = BooleanField(null=False, default=False, verbose_name=u'Аккаунт адміністратора',
                            help_text=u'Відмітьте це поле якщо бажаєте створити нового адміністратора')
    registered_at = DateTimeField(default=datetime.datetime.now, verbose_name=u'Дата і час регістрації')
    confirmed_at = DateTimeField(null=True, verbose_name=u'Дата і час пітведження')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def validate_password(password):
        if not password:
            return False
        if len(password) < MIN_PASSWORD_LENGTH:
            return False
        if password.isdigit():
            return False
        prev_char = password[0]
        for c in password:
            if c != prev_char:
                return True
            prev_char = c
        return False
