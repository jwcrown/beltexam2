# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
import datetime
from django.contrib import messages
from ..login_app.models import User
from models import Trip


# Create your views here.
def index(request):
    if 'username' not in request.session:
        return redirect('/main')
    list = {
        "mytrips": Trip.objects.filter(attendees = request.session['id']).order_by('start_date'),
        "othertrips": Trip.objects.exclude(attendees = request.session['id']).order_by('start_date'),
    }
    return render(request, 'dashboard/index.html', list)

def add(request):
    if 'username' not in request.session:
        return redirect('/main')
    return render(request, 'dashboard/add.html')

def upload(request):
    if 'username' not in request.session:
        return redirect('/main')
    results = Trip.objects.tripvalidate(request.POST)
    if results['status'] == True:
        new_trip = Trip.objects.create_trip(request.POST, request.session['id'])
        return redirect('/travels')
    else:
        for error in results['errors']:
            messages.error(request, error)
    return redirect('/travels/add')

def join(request, trip_id):
    if 'username' not in request.session:
        return redirect('/main')
    attendee = User.objects.get(id = request.session['id'])
    attendee.trips.add(trip_id)
    attendee.save()
    return redirect('/travels')

def show(request, trip_id):
    if 'username' not in request.session:
        return redirect('/main')
    trip = {
        "trip": Trip.objects.get(id = trip_id),
        "attendees": User.objects.filter(trips = trip_id).exclude(uploaded_trips = Trip.objects.get(id =trip_id)),
    }
    return render(request, 'dashboard/show.html', trip)