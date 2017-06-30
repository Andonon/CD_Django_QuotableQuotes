"""
This is the main model.py file for the Quotes app. All validations are done here.
Three functions... insert a quote, add or remove favorite. 
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..login.models import User

class QuoteManager(models.Manager):
    def insertnewquote(self, postData):
        """data validations on new quotes being added. """
        results = {'status': True, 'errors': []}
        if not postData['quoteby'] or len(postData['quoteby']) < 3:
            results['errors'].append("Quoted By must be at least 3 characters")
            results['status'] = False
        if not postData['quotemessage'] or len(postData['quotemessage']) < 10:
            results['errors'].append("Quote Message must be at least 10 characters")
            results['status'] = False
        if results['status'] is False:
            return results
        user = User.objects.get(id=postData['createdBy'])
        newquotecreate = Quote.objects.create(
            quoted_by=postData['quoteby'],
            message=postData['quotemessage'],
            created_by=user)
        return results

    def insertfavorite(self, postData):
        """ moves a quote to the users favorites."""
        results = {'status': True, 'errors': []}
        user = User.objects.get(id=postData['createdBy'])
        quote = Quote.objects.get(id=postData['quoteid'])
        quote.favorite.add(user.id)
        return results

    def removefavorite(self, postData):
        """ moves a quote back to the main library """
        results = {'status': True, 'errors': []}
        user = User.objects.get(id=postData['createdBy'])
        quote = Quote.objects.get(id=postData['quoteid'])
        quote.favorite.remove(user.id)
        return results

class Quote(models.Model):
    quoted_by = models.CharField(max_length=150)
    message = models.CharField(max_length=500)
    created_by = models.ForeignKey(User, related_name="Quotes")
    favorite = models.ManyToManyField(User, related_name="Favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

    def __str__(self):
        return str(self.id)
    