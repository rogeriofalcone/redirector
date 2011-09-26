from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('main.views',
    url(r'^url/list/$', 'url_list', (), 'url_list'),
    url(r'^url/add/$', 'url_add', (), 'url_add'),
    url(r'^url/(?P<url_id>\d+)/edit/$', 'url_edit', (), 'url_edit'),
    url(r'^url/(?P<url_id>\d+)/delete/$', 'url_delete', (), 'url_delete'),
    url(r'^url/multiple/delete/$', 'url_multiple_delete', (), 'url_multiple_delete'),
)
