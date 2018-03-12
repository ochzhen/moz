from peewee import prefetch, fn

from moz import MOZDocument, Category


def is_user_admin(user):
    if user and user.is_authenticated and user.is_admin:
        return True
    return False


def get_categories_with_documents():
    categories = Category.select().order_by(Category.title.asc())
    documents = (MOZDocument.select().order_by(MOZDocument.title.asc()))
    return prefetch(categories, documents)


def get_documents_for_query(query):
    if type(query) == str or type(query) == unicode:
        query = u'%%%s%%' % query  # will build string %query%
        documents = MOZDocument.select().where(MOZDocument.title ** query).order_by(MOZDocument.title.asc())
        if not documents or len(documents) == 0:
            return []
        return documents
    return []
