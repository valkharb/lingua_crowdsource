from django.conf.urls import url
from django.conf.urls import include
from . import views
from django.contrib import admin
from django.conf.urls import *
from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = [

        url(r'^$', views.lit_work_list, name='lit_work_list'),

        # поиск по леммам и текстам
        url(r'^search/$', views.work_filters, name='work_filters'),
        url(r'^search/results/$', views.concordance, name='concordance'),
        url(r'^search/filters/$', views.work_results, name='work_results'),
        url(r'^search/(?P<pk>[0-9]+)/$', views.view_paragraph, name='view_paragraph'),
        url(r'^search/(?P<pk>[0-9]+)/edit/$', views.word_edit, name='markup_edit'),
        url(r'^search/cql/$', views.cql, name='cql'),
        url(r'^search/cql/query$', views.cql_search, name='cql_search'),
        url(r'^search/save/$', views.save_search, name='save_search'),

        # действия в личном кабинете
        url(r'^accounts/', include('registration.urls')),
        url(r'^accounts/(?P<pk>[0-9]+)/$', views.account, name='account'),
        url(r'^accounts/(?P<pk>[0-9]+)/edit/$', views.account_form, name='account_form'),
        url(r'^accounts/login$',  auth_views.LoginView.as_view(), name='login'),
        url(r'^accounts/logout/$', views.logout),

        # регистрация и авторизация
        url(r'^select2/', include('django_select2.urls')),
        url(r'^reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', views.reset_confirm , name='reset_confirm'),
        url(r'^reset/$', views.reset, name='reset'),
        url(r'^accounts/password/reset/$',auth_views.password_reset, {'post_reset_redirect' : '/accounts/password/reset/done/'}),
        url(r'^accounts/password/reset/done/$', auth_views.password_reset_done),
        url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'post_reset_redirect' : '/accounts/password/done/'}, name='password_reset_confirm'),
        url(r'^accounts/password/complete/$', auth_views.password_reset_complete),
        url(r'^admin/(.*)', include(admin.site.urls)),

        # произведение
        url(r'^work/new/$', views.work_new, name='work_new'),
        url(r'^work/(?P<pk>[0-9]+)/$', views.work_detail, name='work_detail'),
        url(r'^work/(?P<pk>[0-9]+)/edit/$', views.work_edit, name='work_edit'),
        url(r'^work/(?P<pk>[0-9]+)/mark/$', views.mark_up, name='mark_up'),
        url(r'^work/(?P<pk>[0-9]+)/sentences/$', views.sentences, name='sentences'),
        url(r'^work/(?P<pk>[0-9]+)/analysis/$', views.analysis, name='analysis'),
        url(r'^work/(?P<pk>[0-9]+)/add_authors/$', views.add_authors, name='add_authors'),

        # коллекции, издательства, вот это вот все
        url(r'^collection/(?P<pk>[0-9]+)/$', views.coll_detail, name='coll_detail'),
        url(r'^publisher/(?P<pk>[0-9]+)/$', views.pub_detail, name='pub_detail'),
        url(r'^authors/(?P<pk>[0-9]+)/$', views.author_detail, name='author_detail'),
        url(r'^authors/$', views.authors_list, name='authors_list'),
        url(r'^authors/new$', views.author_new, name='author_new'),
        url(r'^collections/$', views.collections_list, name='collections_list'),
        url(r'^publishers/$', views.publishers_list, name='publishers_list'),
        url(r'^collection/new/$', views.collection_new, name='collection_new'),
        url(r'^publisher/new/$', views.pub_new, name='pub_new'),


        url(r'^my/$', views.my_works, name='my_lit_works'),

        url(r'^tags/new/(?P<id>[0-9]+)/(?P<type>sentence|word|paragraph|text)/$', views.add_tag, name='add_tag'),

        url(r'^add_mark/(?P<pk>[0-9]+)/(?P<type>work|word)/$', views.add_mark, name='add_mark'),
        url(r'^view_mark/(?P<pk>[0-9]+)/$',views.view_mark, name='view_mark')

    ]