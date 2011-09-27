from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_multi_item_links
from permissions.api import register_permission, set_namespace_title
from project_setup.api import register_setup

from mechanic.models import Link

link_setup = {'text': _(u'intercepted links'), 'view': 'link_list', 'icon': 'telephone_link.png'}#, 'permissions': [PERMISSION_USER_VIEW]}
link_list = {'text': _(u'intercepted links list'), 'view': 'link_list', 'famfam': 'telephone_link'}#, 'permissions': [PERMISSION_USER_VIEW]}
link_add = {'text': _(u'new intercepted link'), 'view': 'link_add', 'famfam': 'telephone_add'}#, 'permissions': [PERMISSION_USER_CREATE]}
link_edit = {'text': _(u'edit'), 'view': 'link_edit', 'args': 'object.id', 'famfam': 'telephone_edit'}#, 'permissions': [PERMISSION_USER_EDIT]}
link_delete = {u'text': _('delete'), 'view': 'link_delete', 'args': 'object.id', 'famfam': 'telephone_delete'}#, 'permissions': [PERMISSION_USER_DELETE]}
link_multiple_delete = {u'text': _('delete'), 'view': 'link_multiple_delete', 'famfam': 'telephone_delete'}#, 'permissions': [PERMISSION_USER_DELETE]}


register_links(Link, [link_edit, link_delete])
register_links(['link_list', 'link_add', 'link_edit', 'link_delete', 'link_multiple_delete'], [link_list, link_add], menu_name=u'sidebar')
register_multi_item_links(['link_list'], [link_multiple_delete])

register_setup(link_setup)
