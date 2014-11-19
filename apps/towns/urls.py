from django.conf.urls import patterns, url

from apps.towns import views

urlpatterns = patterns('',
    #Tavern views
    url(r'^tavern/$', views.tavern, name='tavern'),
    url(r'^outskirts/$', views.outskirts, name='outskirts'),
    url(r'^outskirt/(?P<outskirt_id>\d+)/$', views.outskirt_info, name='outskirt_info'),
    url(r'^tavern/hero/(?P<tavernhero_id>\d+)/$', views.tavern_hero_info, name='tavern_hero_info'),
    
    #town info
    url(r'^town/(?P<slug>[\w-]+)/$', views.town_info, name='town_info'),
)
    

