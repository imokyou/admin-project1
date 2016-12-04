# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^test/', views.test),
    url(r'^$', views.home),
    url(r'^log/(\w+)/', views.log),
    url(r'^news/', views.news),
    url(r'^chat/', views.chat),
    url(r'^mailbox/(\w+)/', views.mailbox)
]
