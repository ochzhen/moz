# coding=utf-8
import flask_login
from flask import request, abort, flash
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.peewee import ModelView
from wtforms.fields import FileField, PasswordField
from wtforms.fields.html5 import EmailField

from models import MOZDocument, Category
from moz import User
from services import is_user_admin
from config import MIN_PASSWORD_LENGTH


class ProtectedIndex(AdminIndexView):

    def is_accessible(self):
        return is_user_admin(flask_login.current_user)

    def inaccessible_callback(self, name, **kwargs):
        abort(403)

    @expose()
    def index(self):
        return self.render(u'admin_index.html')


class ProtectedModelView(ModelView):

    def is_accessible(self):
        return is_user_admin(flask_login.current_user)

    def inaccessible_callback(self, name, **kwargs):
        abort(403)


class CategoryAdmin(ProtectedModelView):
    column_default_sort = ['title']
    column_exclude_list = ['id']
    column_sortable_list = 'title'
    column_searchable_list = ('title', Category.title)
    column_labels = dict(title=Category.title.verbose_name)


class MOZDocumentAdmin(ProtectedModelView):
    column_default_sort = ['creation_date']
    column_exclude_list = ['id']
    column_sortable_list = ('title', 'creation_date')
    column_searchable_list = ('title', MOZDocument.title)
    column_hide_backrefs = False
    column_labels = dict(title=MOZDocument.title.verbose_name,
                         description=MOZDocument.description.verbose_name,
                         creation_date=MOZDocument.creation_date.verbose_name,
                         file=MOZDocument.file.verbose_name,
                         category=MOZDocument.category.verbose_name)
    can_view_details = True
    form_ajax_refs = {
        'category': {
            'fields': (Category.title, 'title')
        }
    }

    form_overrides = dict(file=FileField)

    def create_model(self, form):
        instance = super(MOZDocumentAdmin, self).create_model(form)
        if 'file' in request.files:
            f = request.files['file']
            instance.save_file(f)
        return instance

    def update_model(self, form, model):
        old_file = model.file
        result = super(MOZDocumentAdmin, self).update_model(form, model)
        if 'file' in request.files:
            f = request.files['file']
            model.update_file(f, old_file)
        return result

    def delete_model(self, model):
        file_path = model.file
        result = super(MOZDocumentAdmin, self).delete_model(model)
        if result:
            model.delete_file(file_path)
        return result

class UserAdmin(ProtectedModelView):
    column_default_sort = ['email']
    column_exclude_list = ['id', 'password', 'confirmed_at', 'registered_at', 'speciality', 'occupation']
    column_sortable_list = 'email'
    column_searchable_list = ('email', User.email)
    column_labels = dict(email=User.email.verbose_name,
                         first_name=User.first_name.verbose_name,
                         last_name=User.last_name.verbose_name,
                         active=User.active.verbose_name,
                         is_admin=User.is_admin.verbose_name
                         )
    form_overrides = dict(email=EmailField, password=PasswordField)
    can_view_details = True

    def validate_form(self, form):
        if User.validate_password(form.password.data):
            return super(UserAdmin, self).validate_form(form)
        m = u'Пароль що введено не підпадає під вимоги щодо паролів. ' \
            u'Мінімальна довжина має бути не менеше %d символів. ' \
            u'Пароль не має складатися лише з одного символа що повторюєтся. ' \
            u'Пароль не має містити в собі лише цифри.' % MIN_PASSWORD_LENGTH
        flash(m, category='error')
        return False

    def create_model(self, form):
        instance = super(UserAdmin, self).create_model(form)
        instance.set_password(form.password.data)
        instance.save()
        return instance

    def update_model(self, form, model):
        result = super(UserAdmin, self).update_model(form, model)
        model.set_password(model.password)
        model.save()
        return result
