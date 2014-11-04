from django.conf.urls import patterns, url

from apps.users import views

urlpatterns = patterns('',
    #Authentication urls
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register_user, name='register_user'),
    url(r'^register_succes/$', views.register_succes, name='register succes'),
)

