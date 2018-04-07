# coding: utf-8
import datetime
from flask import current_app, render_template, Blueprint, flash, redirect, url_for, request, abort
from flask_login import current_user, login_user, logout_user, login_required

from moz.auth.email import send_email
from moz.auth.forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm
from moz.auth.token import confirm_token, generate_token

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        from moz.auth.models import User
        user = User.select().where(User.email == form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(u'Невірний email або пароль', 'danger')
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
            speciality=form.speciality.data,
            occupation=form.occupation.data
        )
        user.set_password(form.password.data)
        user.save()

        token = generate_token(user.email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('email/activate.html', confirm_url=confirm_url)
        subject = u'Підтвердження електронної адреси'
        try:
            send_email(user.email, subject, html)
        except Exception as e:
            current_app.logger.error('Email sending error (registration): %s', (e))
            return render_template('500.html')

        login_user(user)

        flash(u'Вітаємо, тепер Ви зареєстрований користувач! Підтвердіть будь ласка свій email.', 'info')
        return redirect(url_for("auth.unconfirmed"))
    return render_template('register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        return redirect(url_for('auth.invalid_link'))
    from moz.auth.models import User
    user = User.select().where(User.email==email).first()

    if user.email != current_user.email:
        return redirect(url_for('auth.invalid_link'))

    if user.active:
        flash(u'Аккаунт вже підтверджено.', 'success')
    else:
        user.confirmed_at = datetime.datetime.now()
        user.active = True
        user.save()
        flash(u'Ви підтвердили свою електронну адресу. Дякуємо!', 'success')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.active:
        return redirect('main.index')
    return render_template('unconfirmed.html')


@auth.route('/resend')
@login_required
def resend_confirmation():
    token = generate_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('email/activate.html', confirm_url=confirm_url)
    subject = u'Підтвердження електронної адреси'
    try:
        send_email(current_user.email, subject, html)
    except Exception as e:
        current_app.logger.error('Email sending error (resending confirmation): %s', (e))
        return render_template('500.html')
    flash(u'Було надіслано нове електронне підтвердження.', 'success')
    return redirect(url_for('auth.unconfirmed'))


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm(request.form)
    if form.validate_on_submit():
        from moz.auth.models import User
        user = User.select().where(User.email == form.email.data).first()
        if user is None:
            form.email.errors.append(u'Користувача з вказаним email не існує.')
            return render_template('forgot_password.html', form=form)
        
        token = generate_token(user.email)
        reset_password_url = url_for('auth.reset_password', token=token, _external=True)
        body = render_template('email/reset_password.html', reset_password_url=reset_password_url)
        subject = u'Відновлення паролю'
        try:
            send_email(user.email, subject, body)
        except Exception as e:
            current_app.logger.error('Email sending error (forgot password): %s', (e))
            return render_template('500.html')
        
        return render_template('reset_link_sent.html')

    return render_template('forgot_password.html', form=form)


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = confirm_token(token)
    except:
        return redirect(url_for('auth.invalid_link'))

    form = ResetPasswordForm(request.form)

    if form.validate_on_submit():
        from moz.auth.models import User
        user = User.select().where(User.email == email).first()
        if user is None:
            return redirect(url_for('auth.invalid_link'))
        user.set_password(form.password.data)
        user.save()

        flash(u'Ваш пароль було змінено. Тепер Ви можете увійти у систему.', 'success')
        if current_user.is_authenticated:
            logout_user()
        return redirect(url_for('auth.login'))
    
    flash(u'Введіть свій новий пароль.', 'info')
    return render_template('reset_password.html', form=form)


@auth.route('/invalid-link')
def invalid_link():
    flash(u'Посилання недійсне або простроченo.', 'danger')
    return render_template('blank.html')
