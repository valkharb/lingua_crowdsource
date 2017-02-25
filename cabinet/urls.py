from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.lit_work_list, name='lit_work_list'),
]