# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils import timezone


class MOZDocument(models.Model):
    class Meta:
        db_table = 'MOZ_DOCUMENT'
        verbose_name_plural = 'Документ МОЗ'
        verbose_name = 'Документи МОЗ'

    title = models.CharField(db_index=True, max_length=256, verbose_name='Заголовок', null=False, blank=False)
    content = models.TextField(null=False, blank=False, verbose_name='Опис')
    document = models.FileField(null=False, blank=False, verbose_name='Документ',
                                upload_to='moz')
    publication_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публікації документу')

    def __unicode__(self):
        return u'%s' % self.title

    def get_document(self):
        if self.document:
            return u'%s' % self.document.url


# Check this small example to understand how we can extend django User model
# Also check docs and this https://habrahabr.ru/post/313764/
# Check that we actually need to do this?
class MOZUser(AbstractUser):
    job_title = models.CharField(default="Doctor", blank=False, max_length=128)
