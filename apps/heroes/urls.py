from django.conf.urls import patterns, url

from apps.heroes import views

urlpatterns = patterns('',
    #Authentication urls
    url(r'^hero/(?P<hero_id>[0-9]+)/$', views.hero, name='hero'),
    url(r'^heroes/$', views.heroes, name='heroes'),
)

