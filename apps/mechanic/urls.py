from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('mechanic.views',
    url(r'^simple/site/(?P<site_domain>[a-zA-Z0-9._]+)/url/(?P<url>.*)$', 'fetch', (), 'fetch'),
    url(r'^simple/site/(?P<site_domain>[a-zA-Z0-9._]+)/$', 'fetch', (), 'fetch'),
    url(r'^simple/(?P<url>.*)$', 'fetch', (), 'fetch'),
    url(r'^simple/$', 'fetch', (), 'fetch'),
    
    url(r'^coded/site/(?P<site_domain>[a-zA-Z0-9._]+)/url/(?P<coded_url>.*)$', 'fetch_coded', (), 'fetch_coded'),
    url(r'^coded/site/(?P<site_domain>[a-zA-Z0-9._]+)/$', 'fetch_coded', (), 'fetch_coded'),
    url(r'^coded/(?P<coded_url>.*)$', 'fetch_coded', (), 'fetch_coded'),
    url(r'^coded/$', 'fetch_coded', (), 'fetch_coded'),
)
