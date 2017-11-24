# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..login_app.models import User
import datetime
from django.db import models


# Create your models here.
class TripManager(models.Manager):
    def create_trip(self, postData, user_id):
        new_trip = self.create(destination = postData['destination'], start_date = postData['start_date'], end_date = postData['end_date'], plan = postData['plan'], uploader = User.objects.get(id = user_id))
        attendee = User.objects.get(id = user_id)
        attendee.trips.add(new_trip)
        attendee.save()
        return new_trip

    def tripvalidate(self, postData):
        now = str(datetime.datetime.now())
        results = {'status': True, 'errors': []}
        if len(postData['destination']) < 1:
            results['errors'].append('Destination field cannot be empty')
            results['status'] = False        
        if len(postData['plan']) < 1:
            results['errors'].append('Description field cannot be empty')
            results['status'] = False
        if len(postData['start_date']) < 1:
            results['errors'].append('Travel Date From field cannot be empty')
            results['status'] = False
        elif postData['start_date'] < now:
            results['errors'].append('Travel Date From must be in the future')
            results['status'] = False
        if len(postData['end_date']) < 1:
            results['errors'].append('Travel Date To field cannot be empty')
            results['status'] = False
        elif postData['end_date'] < postData['start_date']:
            results['errors'].append('Travel Date To must be after Travel Date From')
            results['status'] = False
        return results
        
class Trip(models.Model):
    destination = models.CharField(max_length =255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.CharField(max_length =255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    uploader = models.ForeignKey(User, related_name="uploaded_trips")
    attendees = models.ManyToManyField(User, related_name="trips")
    objects = TripManager()
