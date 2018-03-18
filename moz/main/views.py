import os

from flask import render_template, Blueprint, current_app, send_from_directory, request, abort
from flask_login import login_required

from moz.auth.email import confirmed_email
from moz import app
from services import get_categories_with_documents, get_documents_for_query

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return render_template('home.html')


@main.route('/documents')
@login_required
@confirmed_email
def documents_list():
    categories_with_documents = get_categories_with_documents()
    current_app.logger.info("Found categories with documents %s for template documents_list.html",
                            categories_with_documents)
    return render_template('documents_list.html', categories=categories_with_documents)


@main.route('/documents/<int:id>')
@login_required
def view_document(id):
    return render_template('document.html')


@main.route(app.config.get('MEDIA_URL') + '/<filename>')
@login_required
def get_moz_document(filename):
    folder = os.path.join(app.config.get('MEDIA_ROOT'), 'moz')
    current_app.logger.info("Looking for file %s in folder %s", filename, folder)
    return send_from_directory(folder, filename)


@main.route('/search')
@login_required
def search():
    query = request.args.get('query')
    query = query if query else ""
    query = u"%s" % query
    documents = get_documents_for_query(query)
    current_app.logger.info(u"Found documents: %s for query: %s", documents, query)
    return render_template('search.html', query=query, documents=documents)


@main.errorhandler(404)
def not_found(error):
    return render_template('404.html')
