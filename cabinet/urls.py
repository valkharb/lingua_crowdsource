from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.lit_work_list, name='lit_work_list'),
        url(r'^work/(?P<pk>[0-9]+)/$', views.work_detail, name='work_detail'),
        url(r'^work/new/$', views.work_new, name='work_new'),
        url(r'^work/(?P<pk>[0-9]+)/edit/$', views.work_edit, name='work_edit'),
        url(r'^work/(?P<pk>[0-9]+)/mark/$', views.mark_up, name='mark_up'),
        # url(r'^search/$', views.work_search, name='work_search'),
        url(r'^search/filters/$', views.work_filters, name='work_filters'),
    ]