from flask import render_template, Blueprint, current_app
from flask_login import login_required

from moz.auth.email import confirmed_email

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    current_app.logger.debug("Hello %s", "world")
    return render_template('home.html')


@main.route('/documents')
@login_required
@confirmed_email
def documents_list():
    return render_template('documents_list.html')


@main.route('/documents/<int:id>')
@login_required
def view_document(id):
    return render_template('document.html')


@main.errorhandler(404)
def not_found(error):
    return render_template('404.html')
