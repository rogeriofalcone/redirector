from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('cms.views',
    url(r'^list/$', 'page_list', (), 'page_list'),
    url(r'^add/$', 'page_add', (), 'page_add'),
    url(r'^(?P<page_id>\d+)/edit/$', 'page_edit', (), 'page_edit'),
    url(r'^(?P<page_id>\d+)/delete/$', 'page_delete', (), 'page_delete'),
    url(r'^multiple/delete/$', 'page_multiple_delete', (), 'page_multiple_delete'),
    url(r'^(?P<page_id>\d+)/render/$', 'page_view', {'preview':False}, 'page_render'),
    url(r'^(?P<page_id>\d+)/preview/$', 'page_view', {'preview':True}, 'page_preview'),
)
