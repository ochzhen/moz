# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, u'home.html', {})


def error404(request):
    response = render(request, u'404.html', {})
    response.status_code = 404
    return response
