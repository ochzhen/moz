# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from models import MOZDocument, MOZUser
from django.conf import settings


# Register your models here.
class MOZDocumentAdmin(admin.ModelAdmin):
    model = MOZDocument
    search_fields = ['title']
    list_filter = ('title', 'publication_date')


admin.site.register(MOZDocument, MOZDocumentAdmin)
admin.site.register(MOZUser, UserAdmin)
