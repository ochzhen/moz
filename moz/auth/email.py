from flask import url_for
from flask_mail import Message
from werkzeug.utils import redirect

from moz import app, mail
from flask_login import current_user


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


def confirmed_email(func):
    def func_wrapper():
        if current_user.confirmed_at is not None:
            return func
        else:
            return redirect(url_for('auth.unconfirmed'))
    return func_wrapper
