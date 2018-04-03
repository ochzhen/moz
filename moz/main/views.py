import os

from datetime import datetime, timedelta
from flask import render_template, Blueprint, current_app, send_from_directory, request, abort, make_response
from flask_login import login_required

from config import PROTOCOL, DOMAIN
from moz import app
from moz.auth.email import check_confirmed
from services import get_categories_with_documents, get_documents_for_query

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return render_template('home.html')


@main.route('/documents')
@login_required
@check_confirmed
def documents_list():
    categories_with_documents = get_categories_with_documents()
    current_app.logger.info("Found categories with documents %s for template documents_list.html",
                            categories_with_documents)
    return render_template('documents_list.html', categories=categories_with_documents)


@main.route('/documents/<int:id>')
@login_required
@check_confirmed
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
@check_confirmed
def search():
    query = request.args.get('query')
    query = query if query else ""
    query = u"%s" % query
    documents = get_documents_for_query(query)
    current_app.logger.info(u"Found documents: %s for query: %s", documents, query)
    return render_template('search.html', query=query, documents=documents)


@main.route('/terms_of_use')
def terms_of_use():
    return render_template('terms_of_use.html')

@main.route('/sitemap.xml', methods=['GET'])
def sitemap():
    try:
        pages = []
        ten_days_ago = (datetime.now() - timedelta(days=7)).date().isoformat()
        for rule in app.url_map.iter_rules():
            if "GET" in rule.methods and len(rule.arguments) == 0 and 'admin' not in rule.rule:
                pages.append(
                    [PROTOCOL + DOMAIN + str(rule.rule), ten_days_ago]
                )

        sitemap_xml = render_template('sitemap_template.xml', pages=pages)
        response = make_response(sitemap_xml)
        response.headers["Content-Type"] = "application/xml"

        return response
    except Exception as e:
        return str(e)


@app.route('/robots.txt')
def static_from_root():
 return send_from_directory(app.static_folder, request.path[1:])