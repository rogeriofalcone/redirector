from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('mechanic.views',
    url(r'^simple/(?P<url>.*)/$', 'fetch', (), 'fetch'),
    url(r'^simple_point/(?P<origin_id>\d+)/url/(?P<url>.*)/$', 'fetch', (), 'fetch'),
    url(r'^simple/$', 'fetch', (), 'fetch'),
    url(r'^simple_point/(?P<origin_id>\d+)/$', 'fetch', (), 'fetch'),
    
    url(r'^coded/(?P<coded_url>.*)/$', 'fetch_coded', (), 'fetch_coded'),
    url(r'^coded_point/(?P<origin_id>\d+)/url/(?P<coded_url>.*)/$', 'fetch_coded', (), 'fetch_coded'),
    url(r'^coded/$', 'fetch_coded', (), 'fetch_coded'),
    url(r'^coded_point/(?P<origin_id>\d+)/$', 'fetch_coded', (), 'fetch_coded'),
)
