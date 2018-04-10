from peewee import prefetch

from moz import MOZDocument, Category


def is_user_admin(user):
    return user and user.is_authenticated and user.is_admin


def get_categories_with_documents():
    categories = Category.select().order_by(Category.title.asc())
    documents = (MOZDocument.select().order_by(MOZDocument.title.asc()))
    return prefetch(categories, documents)


def get_documents_for_query(query):
    if type(query) == str or type(query) == unicode:
        query = u'%%%s%%' % query
        documents = MOZDocument.select().where(MOZDocument.title.contains(query)).order_by(MOZDocument.title.asc())
        if not documents or len(documents) == 0:
            return []
        return documents
    return []

def get_document_by_id(id):
    return MOZDocument.select().where(MOZDocument.id == id).first()
