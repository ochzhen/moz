from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    full_name = StringField('Full name')
    education = StringField('Education')
    occupation = StringField('Occupation')
    terms = BooleanField("I agree with terms of use")
    is_medical = BooleanField("I confirm that I'm medical worker")
    submit = SubmitField('Register')

    def validate_email(self, email):
        from moz.auth.models import User
        user = User.select().where((User.email==email.data)).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')