# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^test/$', views.test),
    url(r'^create/$', views.create),
    url(r'^edit/$', views.edit),
    url(r'^detail/$', views.detail),
    url(r'^oplog/$', views.oplog),
    url(r'^revenue/$', views.revenue),
    url(r'^payment/$', views.payment),
    url(r'^payment-success/$', views.payment_success),
    url(r'^relation/$', views.relation),
    url(r'^mailbox/$', views.mailbox),
    url(r'^mailinfo/(\d)/$', views.mailinfo),
    url(r'^mailreply/(\d)/$', views.mailreply),
    url(r'^mail/drop/(\d)/$', views.maildrop),
    url(r'^feedback/$', views.feedback),
    url(r'^feedback/info/(\d)/$', views.feedback_info),
    url(r'^feedback/drop/(\d)/$', views.feedback_drop),
    url(r'^withdraw/$', views.withdraw),
    url(r'^withdraw/pass/(\d)/$', views.withdraw_pass),
    url(r'^withdraw/reject/(\d)/$', views.withdraw_reject),
    url(r'^visa-apply/$', views.visa_apply),
     url(r'^visa-apply/detail/(\d)/$', views.visa_detail),
      url(r'^visa-apply/update/(\d)/$', views.visa_update),
]
