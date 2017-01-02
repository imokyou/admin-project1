# coding=utf-8
from django.conf.urls import include, url
from django.contrib import admin
import app.frontend.views
admin.autodiscover()

# 总的URL设置,新版本按下面的来不会有warning.
urlpatterns = [
    # 改成下面这种分APP的形式了.
    url(r'^$', app.frontend.views.home),
    url(r'^about-us/', app.frontend.views.about_us),
    url(r'^register/', app.frontend.views.register),
    url(r'^login/', app.frontend.views.login),
    url(r'^logout/', app.frontend.views.logout),
    url(r'^video/', app.frontend.views.video),
    url(r'^faq/', app.frontend.views.faq),
    url(r'^support/', app.frontend.views.support),
    url(r'^risk-disclosure/', app.frontend.views.risk_disclosure),
    url(r'^privacy/', app.frontend.views.privacy),
    url(r'^contract/', app.frontend.views.contract),
    url(r'^copyright/', app.frontend.views.copyright),
    url(r'^member/', include('app.member.urls')),
    url(r'^data/', include('app.data.urls')),
    url(r'^backend/', include('app.backend.urls')),
    url(r'^redactor/', include('app.redactor.urls')),
]
