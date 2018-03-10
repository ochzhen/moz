from django.forms import forms
from django.forms import EmailField, CharField, BooleanField, PasswordInput, EmailInput, CheckboxInput


class SigninForm(forms.Form):
    email = EmailField(widget=EmailInput(attrs={'class': 'form-control',
                                                'id': 'email'}), label='Email address:')
    password = CharField(widget=PasswordInput(
        attrs={'class': 'form-control',
               'id': 'pwd'}
    ), label='Password:')
    remember_me = BooleanField(widget=CheckboxInput(), label="Remember me")
