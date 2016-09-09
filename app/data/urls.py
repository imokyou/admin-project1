from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.test),
    url(r'^test', views.test)
]