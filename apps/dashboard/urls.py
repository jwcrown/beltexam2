# DASHBOARD APP LEVEL
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^add$', views.add),
    url(r'^upload$', views.upload),
    url(r'^join/(?P<trip_id>\d+)$', views.join),
    url(r'^destination/(?P<trip_id>\d+)$', views.show),
]