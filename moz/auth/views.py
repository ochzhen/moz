# coding: utf-8
from datetime import datetime
from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from flask_security.confirmable import generate_confirmation_token

from moz.auth.email import send_email
from moz.auth.forms import LoginForm, RegisterForm
from moz.auth.token import confirm_token

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        from moz.auth.models import User
        user = User.select().where((User.email == form.email.data)).first()
        if user is None or not user.check_password(form.password.data):
            flash(u'Невірний email або пароль')
            return render_template('login.html', form=form)
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        from moz.auth.models import User
        user = User(email=form.email.data,
                    active=False,
                    is_admin=False,
                    registered_at=datetime.now(),
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    speciality=form.education.data,
                    occupation=form.occupation.data
        )
        user.set_password(form.password.data)
        user.save()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        html = render_template('confirm.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)

        login_user(user)

        flash('A confirmation email has been sent via email.', 'success')
        flash('Congratulations, you are now a registered user!')
        # return redirect(url_for('auth.login'))
        return redirect(url_for("main.index"))
    return render_template('register.html', title='Register', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    from moz.auth.models import User
    user = User.select().where((User.email == email)).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        user.save()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    flash('Please confirm your account!', 'warning')
    return render_template('unconfirmed.html')