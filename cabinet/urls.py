from django.conf.urls import url
from django.conf.urls import include
from . import views
from django.contrib import admin
from django.conf.urls import *
from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [
        url(r'^select2/', include('django_select2.urls')),
        url(r'^reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
            views.reset_confirm , name='reset_confirm'),
        url(r'^reset/$', views.reset, name='reset'),
        url(r'^accounts/password/reset/$',
                auth_views.password_reset,
                {'post_reset_redirect' : '/accounts/password/reset/done/'}),
        url(r'^accounts/password/reset/done/$',
                auth_views.password_reset_done),
        url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                auth_views.password_reset_confirm,
                {'post_reset_redirect' : '/accounts/password/done/'}),
        url(r'^accounts/password/complete/$',
                auth_views.password_reset_complete),
        url(r'^admin/(.*)', include(admin.site.urls)),
        url(r'^accounts/', include('registration.urls')),
        url(r'^accounts/(?P<pk>[0-9]+)/$', views.account, name='account'),
        url(r'^accounts/(?P<pk>[0-9]+)/edit/$', views.account_form, name='account_form'),
        url(r'^accounts/login$',  auth_views.LoginView.as_view(), name='login'),
        url(r'^accounts/logout/$', views.logout),
        url(r'^$', views.lit_work_list, name='lit_work_list'),
        url(r'^work/(?P<pk>[0-9]+)/$', views.work_detail, name='work_detail'),
        url(r'^authors/$', views.authors_list, name='authors_list'),
        url(r'^collections/$', views.collections_list, name='collections_list'),
        url(r'^publishers/$', views.publishers_list, name='publishers_list'),
        url(r'^work/new/$', views.work_new, name='work_new'),
        url(r'^work/(?P<pk>[0-9]+)/edit/$', views.work_edit, name='work_edit'),
        url(r'^work/(?P<pk>[0-9]+)/mark/$', views.mark_up, name='mark_up'),
        url(r'^search/$', views.work_filters, name='work_filters'),
        url(r'^search/filters/$', views.work_results, name='work_results'),
    ]