from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('mechanic.views',
    url(r'^simple/site/(?P<site_domain>[a-zA-Z0-9._]+)/url/(?P<url>.*)$', 'fetch', (), 'fetch'),
    url(r'^simple/site/(?P<site_domain>[a-zA-Z0-9._]+)/$', 'fetch', (), 'fetch'),
    url(r'^simple/url/(?P<url>.*)$', 'fetch', (), 'fetch'),
    url(r'^simple/$', 'fetch', (), 'fetch'),
    
    url(r'^coded/site/(?P<site_domain>[a-zA-Z0-9._]+)/url/(?P<coded_url>.*)$', 'fetch_coded', (), 'fetch_coded'),
    url(r'^coded/site/(?P<site_domain>[a-zA-Z0-9._]+)/$', 'fetch_coded', (), 'fetch_coded'),
    url(r'^coded/url/(?P<coded_url>.*)$', 'fetch_coded', (), 'fetch_coded'),
    url(r'^coded/$', 'fetch_coded', (), 'fetch_coded'),
    
    url(r'^link/list/$', 'link_list', (), 'link_list'),
    url(r'^link/add/$', 'link_add', (), 'link_add'),
    url(r'^link/(?P<link_id>\d+)/edit/$', 'link_edit', (), 'link_edit'),
    url(r'^link/(?P<link_id>\d+)/delete/$', 'link_delete', (), 'link_delete'),
    url(r'^link/multiple/delete/$', 'link_multiple_delete', (), 'link_multiple_delete'),    
)
