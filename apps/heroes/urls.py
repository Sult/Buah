from django.conf.urls import patterns, url

from apps.heroes import views

urlpatterns = patterns('',
    #Authentication urls
    url(r'^hero/(?P<hero_id>[0-9]+)/$', views.view_hero, name='view_hero'),
    url(r'^heroes/$', views.view_heroes, name='view_heroes'),
)

