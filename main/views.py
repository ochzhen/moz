from flask import render_template, Blueprint, current_app

main = Blueprint('main', __name__,
                 template_folder='templates')


@main.route('/')
def index():
    current_app.logger.debug("Hello %s", "world")
    return render_template('home.html')


@main.route('/register')
def register():
    return render_template('register.html')


@main.route('/login')
def login():
    return render_template('login.html')


@main.route('/documents')
def documents_list():
    return render_template('documents_list.html')


@main.route('/documents/<int:id>')
def view_document(id):
    return render_template('document.html')
