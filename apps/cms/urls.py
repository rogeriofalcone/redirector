from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('cms.views',
    url(r'^page/list/$', 'page_list', (), 'page_list'),
    url(r'^page/add/$', 'page_add', (), 'page_add'),
    url(r'^page/(?P<page_id>\d+)/edit/$', 'page_edit', (), 'page_edit'),
    url(r'^page/(?P<page_id>\d+)/delete/$', 'page_delete', (), 'page_delete'),
    url(r'^page/multiple/delete/$', 'page_multiple_delete', (), 'page_multiple_delete'),
    #url(r'^(?P<page_name>\w+)/render/$', 'page_view', {'preview':False}, 'page_render'),
    #url(r'^(?P<page_name>[A-Z0-9][a-zA-Z0-9-]+)/render/$', 'page_view', {'preview':False}, 'page_render'),
    #url(r'^(?P<slugs>[a-zA-Z0-9-_]+)/render/$', 'page_view', {'preview':False}, 'page_render'),
    url(r'^page/render/by/name/(?P<slug>.*)$', 'page_view', {'preview':False}, 'page_render'),
    url(r'^page/render/by/id/(?P<page_id>\d+)$', 'page_view', {'preview':False}, 'page_render'),
    url(r'^page/(?P<page_id>\d+)/preview/$', 'page_view', {'preview':True}, 'page_preview'),
    
    url(r'^media/list/$', 'media_list', (), 'media_list'),
    url(r'^media/add/$', 'media_add', (), 'media_add'),
    #url(r'^media/(?P<media_id>\d+)/edit/$', 'media_edit', (), 'media_edit'),
    #rl(r'^media/(?P<media_id>\d+)/delete/$', 'media_delete', (), 'media_delete'),
    #url(r'^media/multiple/delete/$', 'media_multiple_delete', (), 'media_multiple_delete'),    
)
