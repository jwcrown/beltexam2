# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

# Create your models here.


class UserManager(models.Manager):
    def validate(self, postData):
        results = {'status': True, 'errors': []}
        if len(postData['name']) < 3:
            results['errors'].append('Your name must have at least 3 characters.')
            results['status'] = False
        if not re.match("^[a-zA-Z ]*$", postData['name']):
            results['errors'].append('Name cannot contain numbers or special characters')
            results['status'] = False
        if len(postData['username']) < 3:
            results['errors'].append('Your username must have at least 3 characters.')
            results['status'] = False
        if len(postData['password']) < 8:
            results['errors'].append('Password must contain at least 8 characters.')
            results['status'] = False
        if postData['password'] != postData['c_password']:
            results['errors'].append('Passwords do not match')
            results['status'] = False
        if len(self.filter(username = postData['username'])) > 0:
            results['errors'].append('Username entered is already registered. Please login.')
            results['status'] = False
        return results

    def creator(self, postData):
        user = self.create(name = postData['name'], username = postData['username'], password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
        return user

    def loginVal(self, postData):
        results = {'status': True, 'errors': [], 'user': None}
        users = self.filter(username = postData['username'])
        if len(users) < 1:
            results['status'] = False
        else:
            if bcrypt.checkpw(postData['password'].encode(), users[0].password.encode()):
                results['user'] = users[0]
            else:
                results['status'] = False
        return results
            


class User(models.Model):
    name = models.CharField(max_length =255)
    username = models.CharField(max_length =255)
    password = models.CharField(max_length =255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()