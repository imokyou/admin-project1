# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^create/', views.create),
    url(r'^test/', views.test),
    url(r'^category/$', views.category_home),
    url(r'^category/create/', views.category_create),
    url(r'^category/edit/', views.category_edit),
]
