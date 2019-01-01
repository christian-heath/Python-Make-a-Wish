from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^wishes$', views.wishes),
    url(r'^hacker$', views.hacker),
    url(r'^new$', views.new),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^stats$', views.stats),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^new_wish$', views.new_wish),
     url(r'^grant$', views.grant),
    url(r'^update/(?P<id>\d+)$', views.update),
    url(r'^delete$', views.delete),
    url(r'^like$', views.like)
]