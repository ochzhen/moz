from flask import render_template, Blueprint, current_app


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    current_app.logger.debug("Hello %s", "world")
    return render_template('home.html')


@main.route('/signup')
def signup():
    return render_template('signup.html')


@main.route('/signin')
def signin():
    return render_template('signin.html')


@main.route('/documents')
def documents_list():
    return render_template('documents_list.html')


@main.route('/documents/<int:id>')
def view_document(id):
    return render_template('document.html')


@main.errorhandler(404)
def not_found(error):
    return render_template('404.html')
