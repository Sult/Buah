from django.conf.urls import patterns, include, url

from django.conf import settings

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('apps.users.urls')),
    url(r'^', include('apps.towns.urls')),
    url(r'^', include('apps.heroes.urls')),
    url(r'^', include('apps.features.urls')),
)

#if settings.DEBUG:
    #urlpatterns += patterns('django.views.static',
        #(r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    #)
