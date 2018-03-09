# coding=utf-8
from flask import request
from flask_admin.contrib.peewee import ModelView
from models import MOZDocument
from wtforms.fields import FileField, HiddenField, StringField, DateTimeField
from wtforms.form import Form


class MOZDocumentAdmin(ModelView):
    column_default_sort = ['creation_date']
    column_exclude_list = ['id']
    column_sortable_list = ('title', 'creation_date')
    column_searchable_list = ('title', MOZDocument.title)

    def get_form(self, adding=True):
        class MOZDocumentForm(Form):
            title = StringField()
            description = StringField()
            file = HiddenField()
            file_file = FileField(u'МОЗ Документ')

        return MOZDocumentForm

    def create_model(self, form):
        instance = super(MOZDocumentAdmin, self).create_model(form)
        if 'file_file' in request.files:
            file = request.files['file_file']
            instance.save_file(file)
        return instance

    def update_model(self, form, model):
        result = super(MOZDocumentAdmin, self).update_model(form, model)
        if 'file_file' in request.files:
            file = request.files['file_file']
            model.update_file(file)
        return result

    def delete_model(self, model):
        file_path = model.file
        result = super(MOZDocumentAdmin, self).delete_model(model)
        if result:
            model.delete_file(file_path)
