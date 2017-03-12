from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.lit_work_list, name='lit_work_list'),
        url(r'^work/(?P<pk>[0-9]+)/$', views.work_detail, name='work_detail'),
    ]