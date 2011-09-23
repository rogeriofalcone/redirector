from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_multi_item_links
from permissions.api import register_permission, set_namespace_title
from project_setup.api import register_setup

from menu_manager.models import MenuEntry

#PERMISSION_USER_CREATE = {'namespace': 'user_management', 'name': 'user_create', 'label': _(u'Create new users')}
#PERMISSION_USER_EDIT = {'namespace': 'user_management', 'name': 'user_edit', 'label': _(u'Edit existing users')}
#PERMISSION_USER_VIEW = {'namespace': 'user_management', 'name': 'user_view', 'label': _(u'View existing users')}
#PERMISSION_USER_DELETE = {'namespace': 'user_management', 'name': 'user_delete', 'label': _(u'Delete existing users')}

#set_namespace_title('user_management', _(u'User management'))
#register_permission(PERMISSION_USER_CREATE)
#register_permission(PERMISSION_USER_EDIT)
#register_permission(PERMISSION_USER_VIEW)
#register_permission(PERMISSION_USER_DELETE)

menu_list = {'text': _(u'root menu list'), 'view': 'menu_list', 'famfam': 'tab_go'}#, 'permissions': [PERMISSION_USER_VIEW]}
menu_add = {'text': _(u'new root menu'), 'view': 'menu_add', 'famfam': 'tab_add'}#, 'permissions': [PERMISSION_USER_CREATE]}
menu_edit = {'text': _(u'edit'), 'view': 'menu_edit', 'args': 'object.id', 'famfam': 'tab_edit'}#, 'permissions': [PERMISSION_USER_EDIT]}
menu_delete = {u'text': _('delete'), 'view': 'menu_delete', 'args': 'object.id', 'famfam': 'tab_delete'}#, 'permissions': [PERMISSION_USER_DELETE]}
menu_multiple_delete = {u'text': _('delete'), 'view': 'menu_multiple_delete', 'famfam': 'tab_delete'}#, 'permissions': [PERMISSION_USER_DELETE]}
menu_add_child = {'text': _(u'new menu entry'), 'view': 'menu_add_child', 'args': 'object.id', 'famfam': 'tab_add'}#, 'permissions': [PERMISSION_USER_CREATE]}
menu_setup = {'text': _(u'menus'), 'view': 'menu_list', 'icon': 'menu.png'}#, 'permissions': [PERMISSION_USER_VIEW]}

register_links(MenuEntry, [menu_edit, menu_delete, menu_add_child])
register_links(['menu_list', 'menu_details', 'menu_add', 'menu_add_child', 'menu_edit', 'menu_delete', 'menu_multiple_delete'], [menu_list, menu_add], menu_name=u'sidebar')
register_multi_item_links(['menu_list'], [menu_multiple_delete])

register_setup(menu_setup)

