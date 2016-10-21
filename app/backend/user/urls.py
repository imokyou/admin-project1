# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^test/', views.test),
    url(r'^create/', views.create),
    url(r'^edit/', views.edit),
    url(r'^detail/', views.detail),
    url(r'^oplog/', views.oplog),
    url(r'^revenue/', views.revenue),
    url(r'^payment/', views.payment),
    url(r'^relation/', views.relation),
]
