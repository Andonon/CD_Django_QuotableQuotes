# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User


# Create your views here.
def index(request):
    # testdelete = User.objects.all().delete()
    if request.session.get('id'):
        return redirect('quotes:index')

    return render(request, 'login/index.html')


def register(request):
    results = User.objects.registervalidate(request.POST)
    if not results['status']:
        for error in results['errors']:
            messages.error(request, error)
            return redirect('auth:index')
    request.session['id'] = results['user'].id
    return redirect('quotes:index')


def login(request):
    results = User.objects.loginvalidate(request.POST)
    if results['status'] is False:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('auth:index')
    else:
        user = User.objects.get(id=results['user'])
        request.session['id'] = user.id
    return redirect('quotes:index')


def logout(request):
    request.session.flush()
    messages.success(request, 'Logged Out')
    return redirect('auth:index')
