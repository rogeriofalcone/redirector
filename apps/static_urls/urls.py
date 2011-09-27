from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('static_urls.views',
    url(r'^list/$', 'url_list', (), 'url_list'),
    url(r'^add/$', 'url_add', (), 'url_add'),
    url(r'^(?P<url_id>\d+)/edit/$', 'url_edit', (), 'url_edit'),
    url(r'^(?P<url_id>\d+)/delete/$', 'url_delete', (), 'url_delete'),
    url(r'^multiple/delete/$', 'url_multiple_delete', (), 'url_multiple_delete'),
)
