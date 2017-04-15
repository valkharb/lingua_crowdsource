from django.conf.urls import url
from django.conf.urls import include
from . import views
from django.contrib import admin
from django.conf.urls import *
from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [
        url(r'^admin/(.*)', include(admin.site.urls)),
        url(r'^accounts/', include('registration.urls')),
        url(r'^accounts/login$',  auth_views.LoginView.as_view(), name='login'),
        url(r'^accounts/logout/$', views.logout),
        url(r'^$', views.lit_work_list, name='lit_work_list'),
        url(r'^work/(?P<pk>[0-9]+)/$', views.work_detail, name='work_detail'),
        url(r'^work/new/$', views.work_new, name='work_new'),
        url(r'^work/(?P<pk>[0-9]+)/edit/$', views.work_edit, name='work_edit'),
        url(r'^work/(?P<pk>[0-9]+)/mark/$', views.mark_up, name='mark_up'),
        url(r'^search/$', views.work_filters, name='work_filters'),
        url(r'^search/filters/$', views.work_results, name='work_results'),
    ]