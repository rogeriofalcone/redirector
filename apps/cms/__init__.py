from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_multi_item_links
from permissions.api import register_permission, set_namespace_title
from project_setup.api import register_setup

from cms.models import Page, Media

page_setup_link = {'text': _(u'CMS pages'), 'view': 'page_list', 'icon': 'page.png'}#, 'permissions': [PERMISSION_USER_VIEW]}
page_list_link = {'text': _(u'CMS page list'), 'view': 'page_list', 'famfam': 'page'}#, 'permissions': [PERMISSION_USER_VIEW]}
page_add_link = {'text': _(u'new CMS page'), 'view': 'page_add', 'famfam': 'page_add'}#, 'permissions': [PERMISSION_USER_CREATE]}
page_edit_link = {'text': _(u'edit'), 'view': 'page_edit', 'args': 'object.id', 'famfam': 'page_edit'}#, 'permissions': [PERMISSION_USER_EDIT]}
page_delete_link = {u'text': _('delete'), 'view': 'page_delete', 'args': 'object.id', 'famfam': 'page_delete'}#, 'permissions': [PERMISSION_USER_DELETE]}
page_multiple_delete_link = {u'text': _('delete'), 'view': 'page_multiple_delete', 'famfam': 'page_delete'}#, 'permissions': [PERMISSION_USER_DELETE]}
page_render_link = {'text': _(u'render'), 'view': 'page_render', 'args': 'object.id', 'famfam': 'page_lightning'}#, 'permissions': [PERMISSION_USER_EDIT]}
page_preview_link = {'text': _(u'preview'), 'view': 'page_preview', 'args': 'object.id', 'famfam': 'zoom'}#, 'permissions': [PERMISSION_USER_EDIT]}


media_setup_link = {'text': _(u'CMS media'), 'view': 'media_list', 'icon': 'drive.png'}#, 'permissions': [PERMISSION_USER_VIEW]}
media_list_link = {'text': _(u'CMS media list'), 'view': 'media_list', 'famfam': 'drive'}#, 'permissions': [PERMISSION_USER_VIEW]}
media_add_link = {'text': _(u'new CMS media'), 'view': 'media_add', 'famfam': 'drive_add'}#, 'permissions': [PERMISSION_USER_CREATE]}
media_edit_link = {'text': _(u'edit'), 'view': 'media_edit', 'args': 'object.id', 'famfam': 'drive_edit'}#, 'permissions': [PERMISSION_USER_EDIT]}
media_delete_link = {u'text': _('delete'), 'view': 'media_delete', 'args': 'object.id', 'famfam': 'drive_delete'}#, 'permissions': [PERMISSION_USER_DELETE]}
media_multiple_delete_link = {u'text': _('delete'), 'view': 'media_multiple_delete', 'famfam': 'drive_delete'}#, 'permissions': [PERMISSION_USER_DELETE]}
media_preview_link = {'text': _(u'preview'), 'view': 'media_preview', 'args': 'object.id', 'famfam': 'zoom'}#, 'permissions': [PERMISSION_USER_EDIT]}


register_links(Page, [page_preview_link, page_edit_link, page_delete_link, page_render_link])
register_links(['page_list', 'page_add', 'page_edit', 'page_delete', 'page_multiple_delete'], [page_list_link, page_add_link], menu_name=u'sidebar')
register_multi_item_links(['page_list'], [page_multiple_delete_link])

register_setup(page_setup_link)

register_links(Media, [media_edit_link, media_delete_link])
register_links(['media_list', 'media_add', 'media_edit', 'media_delete', 'media_multiple_delete'], [media_list_link, media_add_link], menu_name=u'sidebar')
register_multi_item_links(['media_list'], [media_multiple_delete_link])

register_setup(media_setup_link)
