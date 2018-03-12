from peewee import prefetch

from moz import MOZDocument, Category


def is_user_admin(user):
    if user and user.is_authenticated and user.is_admin:
        return True
    return False


def get_categories_with_documents():
    categories = Category.select().order_by(Category.title.asc())
    documents = (MOZDocument.select().order_by(MOZDocument.title.asc()))
    return prefetch(categories, documents)
