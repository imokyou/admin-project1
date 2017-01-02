# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^test/$', views.test),
    url(r'^change-password/$', views.change_password),
    url(r'^create/$', views.create),
    url(r'^edit/$', views.edit),
    url(r'^detail/$', views.detail),
]
