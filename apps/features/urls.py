from django.conf.urls import patterns, url

from apps.features import views

urlpatterns = patterns('',
    #town
    url(r'^help/(?P<slug>[\w-]+)/$', views.view_help_article, name='view_help_article'),
)
    

