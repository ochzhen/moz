# coding: utf-8
import datetime
from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from moz.auth.email import send_email
from moz.auth.forms import LoginForm, RegisterForm
from moz.auth.token import confirm_token, generate_confirmation_token

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        from moz.auth.models import User
        user = User.select().where((User.email == form.email.data)).first()
        if user is None or not user.check_password(form.password.data):
            flash(u'Невірний email або пароль', category='error')
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
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        from moz.auth.models import User
        user = User(
            email=form.email.data,
            active=False,
            is_admin=False,
            registered_at=datetime.datetime.now(),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            speciality=form.speciality.data,
            occupation=form.occupation.data
        )
        user.set_password(form.password.data)
        user.save()
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = u'Будь ласка, підтвердьте свою електронну пошту'
        send_email(user.email, subject, html)

        login_user(user)

        flash(u'Вітаємо, тепер Ви зареєстрований користувач! Підтвердіть будь ласка свій email')
        return redirect(url_for("auth.unconfirmed"))
    return render_template('register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash(u'Посилання для підтвердження недійсний або простроченo.', 'danger')
    from moz.auth.models import User
    user = User.select().where(User.email==email).get()
    if user.confirmed_at is not None:
        flash(u'Аккаунт вже підтверджено. Будь ласка, увійдіть', 'success')
    else:
        user.confirmed_at = datetime.datetime.now()
        user.save()
        flash(u'Ви підтвердили свою пошту. Дякую!', 'success')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed_at is not None:
        return redirect('main.index')
    flash(u'Будь ласка, підтвердьте свою електронну пошту!', 'warning')
    return render_template('unconfirmed.html')


@auth.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = u'Будь ласка, підтвердьте свою електронну пошту'
    send_email(current_user.email, subject, html)
    flash(u'Було надіслано нове електронне підтвердження.', 'success')
    return redirect(url_for('auth.unconfirmed'))