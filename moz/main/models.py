# coding=utf-8
import datetime
import errno
import os

from peewee import Model, TextField, DateTimeField, CharField, AutoField, ForeignKeyField
from werkzeug.utils import secure_filename

from config import MEDIA_ROOT, MEDIA_URL
from moz import db


class BaseModel(Model):
    class Meta:
        database = db


class Category(BaseModel):
    id = AutoField(null=False, index=True, unique=True, primary_key=True)
    title = CharField(null=False,
                      max_length=256,
                      verbose_name=u"Назва категорії")

    def __unicode__(self):
        return u"%s" % self.title


class MOZDocument(BaseModel):
    id = AutoField(null=False, index=True, unique=True, primary_key=True)

    title = CharField(null=False,
                      max_length=512,
                      help_text=u"Назва файлу що буде відображатися користувачам",
                      verbose_name=u"Заголовок")

    description = TextField(null=False,
                            help_text=u"Опис файлу",
                            verbose_name=u"Опис")  # TODO do we need short description field?

    file = CharField(null=False,
                     max_length=512,
                     verbose_name=u"Файл")

    creation_date = DateTimeField(null=False, default=datetime.datetime.now(), verbose_name=u"Дата публікації")

    category = ForeignKeyField(model=Category,
                               backref='documents',
                               null=False,
                               verbose_name=u'Категорія документа')

    def get_url(self):
        return u"/documents/%s" % self.id

    def save_file(self, file_obj):
        if not os.path.exists(os.path.join(MEDIA_ROOT, 'moz')):
            path = os.path.join(MEDIA_ROOT, 'moz')
            try:
                os.makedirs(path, 0770)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else:
                    raise
        name, extension = os.path.splitext(file_obj.filename)
        self.file = secure_filename(name + datetime.datetime.now().isoformat() + extension)
        full_path = os.path.join(MEDIA_ROOT, 'moz', self.file)
        file_obj.save(full_path)
        return self.save()

    def update_file(self, file_obj, old_file):
        is_saved = self.save_file(file_obj)
        if is_saved and old_file:
            full_path = os.path.join(MEDIA_ROOT, 'moz', old_file)
            if os.path.isfile(full_path):
                os.remove(full_path)
        return is_saved

    def delete_file(self, file_name):
        full_path = os.path.join(MEDIA_ROOT, 'moz', file_name)
        if os.path.isfile(full_path):
            os.remove(full_path)

    def get_file_url(self):
        return os.path.join(MEDIA_URL, self.file)

    def __unicode__(self):
        return u"id=%s title=%s last_update_date=%s" % (self.id, self.title, self.creation_date)
