# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^test/$', views.test),
    url(r'^$', views.home),
    url(r'^bonus/$', views.bonus),
    url(r'^order/$', views.order),
]
