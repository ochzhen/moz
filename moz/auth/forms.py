# coding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length, Regexp
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[DataRequired(message=u'Обов\'язкове поле')]
    )
    password = PasswordField(
        u'Пароль',
        validators=[DataRequired(message=u'Обов\'язкове поле')]
    )
    remember_me = BooleanField(u'Запам\'ятати мене')
    submit = SubmitField(u'Увійти')


class RegisterForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[
            DataRequired(message=u'Обов\'язкове поле'),
            Email(),
            Length(max=100, message=u'Email має бути довжиною не більше 100 символів')
        ]
    )
    password = PasswordField(
        u'Пароль',
        validators=[
            DataRequired(message=u'Обов\'язкове поле'),
            Length(min=8, message=u'Пароль має бути довжиною не менше 8 символів'),
            Regexp(
                regex=r'[A-Za-z0-9@#$%^&+=]+',
                message=u'Пароль має складатися з латинських літер [a-z, A-Z], цифр [0-9] та символів [@, #, $, %, ^, =, &, +]'
            )
        ]
    )
    confirm_password = PasswordField(
        u'Підтвердіть пароль',
        validators=[
            DataRequired(message=u'Обов\'язкове поле'),
            EqualTo('password', message=u'Паролі не співпадають')
        ]
    )
    speciality = StringField(
        u'Спеціальність',
        validators=[
            DataRequired(message=u'Обов\'язкове поле'),
            Length(max=50, message=u'Поле має бути довжиною не більше 50 символів')
        ]
    )
    occupation = StringField(
        u'Місце роботи',
        validators=[
            DataRequired(message=u'Обов\'язкове поле'),
            Length(max=50, message=u'Поле має бути довжиною не більше 50 символів')
        ]
    )
    terms = BooleanField(
        validators=[DataRequired(message=u'Обов\'язкове поле')]
    )
    is_medical = BooleanField(
        u'Я підтверджую, що я медичний працівник.',
        validators=[DataRequired(message=u'Обов\'язкове поле')]
    )
    submit = SubmitField(u'Зареєструвати')

    def validate_email(self, email):
        from moz.auth.models import User
        user = User.select().where((User.email == email.data)).first()
        if user is not None:
            raise ValidationError(u'Користувач з вказаною адресою вже зареєстрований. Використайте іншу електронну адресу.')


class ForgotPasswordForm(FlaskForm):
    email = EmailField(
        'Email',
        validators=[
            DataRequired(message=u'Обов\'язкове поле'),
            Email(),
            Length(max=100, message=u'Email має бути довжиною не більше 100 символів')
        ]
    )
    submit = SubmitField(u'Відправити')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        u'Пароль',
        validators=[
            DataRequired(message=u'Обов\'язкове поле'),
            Length(min=8, message=u'Пароль має бути довжиною не менше 8 символів'),
            Regexp(
                regex=r'[A-Za-z0-9@#$%^&+=]+',
                message=u'Пароль має складатися з латинських літер [a-z, A-Z], цифр [0-9] та символів [@, #, $, %, ^, =, &, +]'
            )
        ]
    )
    confirm_password = PasswordField(
        u'Підтвердіть пароль',
        validators=[
            DataRequired(message=u'Обов\'язкове поле'),
            EqualTo('password', message=u'Паролі не співпадають')
        ]
    )
    submit = SubmitField(u'Відновити')
