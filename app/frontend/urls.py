from django.conf.urls import url
import views

urlpatterns = [
    url(r'^test', views.test),
    url(r'^$', views.home),
    url(r'^about-us/$', views.about_us),
    url(r'^register', views.register),
    url(r'^login', views.login),
    url(r'^video', views.video),
    url(r'^faq', views.faq),
    url(r'^support', views.support),
]
