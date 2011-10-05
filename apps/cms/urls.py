from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('cms.views',
    url(r'^list/$', 'page_list', (), 'page_list'),
    url(r'^add/$', 'page_add', (), 'page_add'),
    url(r'^(?P<page_id>\d+)/edit/$', 'page_edit', (), 'page_edit'),
    url(r'^(?P<page_id>\d+)/delete/$', 'page_delete', (), 'page_delete'),
    url(r'^multiple/delete/$', 'page_multiple_delete', (), 'page_multiple_delete'),
    #url(r'^(?P<page_name>\w+)/render/$', 'page_view', {'preview':False}, 'page_render'),
    #url(r'^(?P<page_name>[A-Z0-9][a-zA-Z0-9-]+)/render/$', 'page_view', {'preview':False}, 'page_render'),
    #url(r'^(?P<slugs>[a-zA-Z0-9-_]+)/render/$', 'page_view', {'preview':False}, 'page_render'),
    url(r'^render/by/name/(?P<slug>.*)$', 'page_view', {'preview':False}, 'page_render'),
    url(r'^render/by/id/(?P<page_id>\d+)$', 'page_view', {'preview':False}, 'page_render'),
    url(r'^(?P<page_id>\d+)/preview/$', 'page_view', {'preview':True}, 'page_preview'),
)
