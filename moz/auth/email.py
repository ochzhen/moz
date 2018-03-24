from functools import wraps

from flask import redirect, url_for
from flask_login import current_user
from flask_mail import Message


def send_email(to, subject, template):
    from moz import app, mail
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.active:
            return redirect(url_for('auth.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function
