from django.conf.urls import patterns, url

from apps.towns import views

urlpatterns = patterns('',
    #town
    url(r'^town/(?P<slug>[\w-]+)/$', views.view_town_info, name='view_town_info'),
    
    #Tavern views
    url(r'^tavern/$', views.tavern, name='tavern'),
    url(r'^tavern/hero/(?P<tavernhero_id>\d+)$', views.tavern_hero_info, name='tavern_hero_info'),
)
    

