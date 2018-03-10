# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from moz.forms import SigninForm
from service import get_all_documents_order_by_title


# Create your views here.

def index(request):
    return render(request, u'home.html', {})


def signin(request):
    form = SigninForm()
    data = {
        'form': form
    }
    return render(request, u'signin.html', data)


def signup(request):
    return render(request, u'signup.html', {})


def documents(request):
    data = {
        'documents': get_all_documents_order_by_title()
    }
    return render(request, 'documents_list.html', data)


def error404(request):
    response = render(request, u'404.html', {})
    response.status_code = 404
    return response
