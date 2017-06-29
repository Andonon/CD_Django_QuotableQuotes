# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from models import Quote

def index(request):
    loggedinuser = User.objects.get(id=request.session['id'])
    favoritequote = Quote.objects.filter(favorite = request.session['id'])
    quotablequotes = Quote.objects.all().exclude(favorite = request.session['id'])
    context = {
        'loggedinuser': loggedinuser,
        'quotablequotes': quotablequotes,
        'favoritequotes': favoritequote
    }
    return render(request, 'quotes/index.html', context)

def newQuote(request):
    insertnewquote = Quote.objects.insertnewquote(request.POST)
    if not insertnewquote['status']:
        for error in insertnewquote['errors']:
            messages.error(request, error)
            return redirect('quotes:newQuote')
    return redirect('quotes:index')

def addFavorite(request):
    insertfavorite = Quote.objects.insertfavorite(request.POST)
    if not insertfavorite['status']:
        for error in insertfavorite['errors']:
            messages.error(request, error)
    return redirect('quotes:index')

def removeFavorite(request):
    removefavorite = Quote.objects.removefavorite(request.POST)
    if not removefavorite['status']:
        for error in removefavorite['errors']:
            messages.error(request, error)
    return redirect('quotes:index')
