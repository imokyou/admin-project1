# coding=utf-8
from django.conf.urls import include, url
import app.backend.admin.views

# 总的URL设置,新版本按下面的来不会有warning.
urlpatterns = [

    # 改成下面这种分APP的形式了.
    url(r'^', include('app.backend.dashboard.urls')),
    url(r'^login/$', app.backend.admin.views.login),
    url(r'^logout/$', app.backend.admin.views.logout),
    url(r'^invite-code/', include('app.backend.invitecode.urls')),
    url(r'^admin/', include('app.backend.admin.urls')),
    url(r'^user/', include('app.backend.user.urls')),
    url(r'^project/', include('app.backend.projects.urls')),
    url(r'^news/', include('app.backend.news.urls')),
    url(r'^statics/', include('app.backend.statics.urls')),
    url(r'^cbcd/', include('app.backend.cbcd.urls')),
]