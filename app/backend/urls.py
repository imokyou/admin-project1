# coding=utf-8
from django.conf.urls import include, url

# 总的URL设置,新版本按下面的来不会有warning.
urlpatterns = [

    # 改成下面这种分APP的形式了.
    url(r'^$', include('app.backend.dashboard.urls')),
    url(r'^invite_code/', include('app.backend.invitecode.urls')),
]