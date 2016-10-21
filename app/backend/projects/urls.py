# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^test', views.test),
    url(r'^$', views.home),
    url(r'^create', views.create),
    url(r'^edit', views.edit)
]
