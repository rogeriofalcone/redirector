from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('menu_manager.views',
    url(r'^menu/list/$', 'menu_list', (), 'menu_list'),
    url(r'^menu/(?P<parent_menu_entry_id>\d+)/list/$', 'menu_list', (), 'menu_details'),
    url(r'^menu/add/$', 'menu_add', (), 'menu_add'),
    url(r'^menu/(?P<parent_menu_entry_id>\d+)/add/$', 'menu_add', (), 'menu_add_child'),
    url(r'^menu/(?P<menu_entry_id>\d+)/edit/$', 'menu_edit', (), 'menu_edit'),
    url(r'^menu/(?P<menu_entry_id>\d+)/delete/$', 'menu_delete', (), 'menu_delete'),
    url(r'^menu/multiple/delete/$', 'menu_multiple_delete', (), 'menu_multiple_delete'),
)
