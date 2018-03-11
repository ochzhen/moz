# coding: utf-8

from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from moz.auth.forms import LoginForm, RegisterForm

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
                    full_name=form.full_name.data,
                    education=form.education.data,
                    occupation=form.occupation.data,
                    terms=form.terms.data,
                    is_medical=form.is_medical.data)
        user.set_password(form.password.data)
        user.save()
        flash(u'Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)
