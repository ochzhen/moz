# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message=u'Обов\'язкове поле')])
    password = PasswordField(u'Пароль', validators=[DataRequired(message=u'Обов\'язкове поле')])
    remember_me = BooleanField(u'Запам\'ятати мене')
    submit = SubmitField(u'Увійти')


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(message=u'Обов\'язкове поле'), Email()])
    password = PasswordField(u'Пароль', validators=[DataRequired(message=u'Обов\'язкове поле')])
    confirm_password = PasswordField(
        u'Підтвердіть пароль', validators=[DataRequired(message=u'Обов\'язкове поле'), EqualTo('password')])
    first_name = StringField(u'Ім\'я', validators=[DataRequired(message=u'Обов\'язкове поле')])
    last_name = StringField(u'Прізвище', validators=[DataRequired(message=u'Обов\'язкове поле')])
    education = StringField(u'Спеціальність', validators=[DataRequired(message=u'Обов\'язкове поле')])
    occupation = StringField(u'Місце роботи', validators=[DataRequired(message=u'Обов\'язкове поле')])
    terms = BooleanField(u'Я погоджуюся з умовами використання.',
                         validators=[DataRequired(message=u'Обов\'язкове поле')])
    is_medical = BooleanField(u'Я підтверджую, що я медичний співробітник.',
                              validators=[DataRequired(message=u'Обов\'язкове поле')])
    submit = SubmitField(u'Зареєструвати')

    def validate_email(self, email):
        from moz.auth.models import User
        user = User.select().where((User.email == email.data)).first()
        if user is not None:
            raise ValidationError(u'Будь ласка використайте іншу почтову адресу.')
