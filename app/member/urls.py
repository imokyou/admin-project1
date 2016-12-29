# coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^test/$', views.test),
    url(r'^$', views.home),
    url(r'^log/(\w+)/$', views.log),
    url(r'^news/$', views.news),
    url(r'^chat/$', views.chat),
    url(r'^mailbox/(\w+)/$', views.mailbox),
    url(r'^rank/$', views.rank),
    url(r'^seller/$', views.seller),
    url(r'^promotion/$', views.promotion),
    url(r'^selling/$', views.selling),
    url(r'^buying/$', views.buying),
    url(r'^change-recommend-user/$', views.change_recommend_user),
    url(r'^setting/$', views.setting),
    url(r'^dashboard/$', views.dashboard),
    url(r'^us-bank-account/$', views.us_bank_account),
    url(r'^withdraw/$', views.withdraw),
    url(r'^bonus/$', views.bonus),
    url(r'^cbcd-price/$', views.cbcd_price),
    url(r'^cbcd-sell/$', views.cbcd_sell),
    url(r'^cbcd-buy/$', views.cbcd_buy),
    url(r'^trading-hall/(\w+)/$', views.trading_hall)
]
