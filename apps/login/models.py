# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from datetime import datetime, timedelta
from django.db import models


# Create your models here.
class UserManager(models.Manager):
    def registervalidate(self, postData):
        results = {'status': True, 'errors': [], 'user': None}
        if not postData['fname'] or len(postData['fname']) < 3:
            results['errors'].append("First Name must be at least 3 characters")
            results['status'] = False
        if not postData['lname'] or len(postData['lname']) < 3:
            results['errors'].append("Last Name must be at least 3 characters")
            results['status'] = False
        if not postData['alias'] or len(postData['alias']) < 3:
            results['errors'].append("Alias must be at least 3 characters")
            results['status'] = False
        if not postData['dob']:
            results['errors'].append("Birthday is required")
            results['status'] = False
        if not postData['userpassword'] or len(postData['userpassword']) < 8:
            results['errors'].append("Password must be at least 8 characters")
            results['status'] = False
        if postData['cpassword'] != postData['userpassword']:
            results['errors'].append("Passwords do not match")
            results['status'] = False
        if results['status'] is False:
            return results
        user = User.objects.filter(alias=postData['alias'])
        if user:
            results['status'] = False
            results['errors'].append("Registration Failure, have you tried to login?")
        if results['status']:
            userpassword = bcrypt.hashpw(postData['userpassword'].encode(), bcrypt.gensalt())
            user = User.objects.create(
                fname=postData['fname'],
                lname=postData['lname'],
                email=postData['email'],
                dob=postData['dob'],
                alias=postData['alias'],
                userpassword=userpassword)
            results['user'] = user
        return results

    def loginvalidate(self, postData):
        results = {'status': True, 'errors': [], 'user': None}
        try:                # need this try loop if the db is empty.
            user = User.objects.filter(alias=postData['alias'])
            user[0]
        except:
            results['status'] = False
            results['errors'].append("Account or password failure.")
            return results
        if user[0]:
            if user[0].userpassword != bcrypt.hashpw(postData['userpassword'].encode(),
                                                     user[0].userpassword.encode()):
                results['status'] = False
                results['errors'].append("Account or password failure.")
            else:
                results['user'] = user[0].id
        else:
            results['status'] = False
        return results


class User(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    alias = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=100, unique=True)
    userpassword = models.CharField(max_length=100)
    dob = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + ", " + self.email
    objects = UserManager()
