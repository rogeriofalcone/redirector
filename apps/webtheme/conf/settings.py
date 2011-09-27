"""Configuration options for the web_bones app"""
from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

from webtheme.literals import TEMPLATE_VIEW_MODE_FULL, \
    TEMPLATE_VIEW_MODE_PLAIN, TEMPLATE_VIEW_MODE_BARE

register_settings(
    namespace=u'webtheme',
    module=u'webtheme.conf.settings',
    settings=[
        {'name': u'WEB_APP_THEME_THEME', 'global_name': u'WEB_BONES_WEB_APP_THEME_THEME', 'default': u'activo', 'description': _(u'CSS theme to apply, options are: amro, bec, bec-green, blue, default, djime-cerulean, drastic-dark, kathleene, olive, orange, red, reidb-greenish and warehouse.')},
        {'name': u'WEB_APP_THEME_SCROLL_JS', 'global_name': u'WEB_BONES_WEB_APP_THEME_SCROLL_JS', 'default': True, 'hidden': True},
        {'name': u'VERBOSE_LOGIN', 'global_name': u'WEB_BONES_VERBOSE_LOGIN', 'default': True, 'description': _(u'Display extra information in the login screen.')},
    ]
)

TEMPLATE_VIEW_MODES = {
    'educational_site': {
        'login': TEMPLATE_VIEW_MODE_BARE,
        'setup_list': TEMPLATE_VIEW_MODE_PLAIN,
        'user_list': TEMPLATE_VIEW_MODE_PLAIN,
        'user_add': TEMPLATE_VIEW_MODE_PLAIN,
        'user_edit': TEMPLATE_VIEW_MODE_PLAIN,
        'user_delete': TEMPLATE_VIEW_MODE_PLAIN,
        'user_set_password': TEMPLATE_VIEW_MODE_PLAIN,
        'group_list': TEMPLATE_VIEW_MODE_PLAIN,
        'group_add': TEMPLATE_VIEW_MODE_PLAIN,
        'group_edit': TEMPLATE_VIEW_MODE_PLAIN,
        'group_delete': TEMPLATE_VIEW_MODE_PLAIN,
        'group_members': TEMPLATE_VIEW_MODE_PLAIN,
        
        'role_list': TEMPLATE_VIEW_MODE_PLAIN,
        'role_permissions': TEMPLATE_VIEW_MODE_PLAIN,
        'role_edit': TEMPLATE_VIEW_MODE_PLAIN,
        'role_create': TEMPLATE_VIEW_MODE_PLAIN,
        'role_delete': TEMPLATE_VIEW_MODE_PLAIN,
        'permission_grant_revoke': TEMPLATE_VIEW_MODE_PLAIN,
        'role_members': TEMPLATE_VIEW_MODE_PLAIN,
    },
    'educational_site_green': {
        'login': TEMPLATE_VIEW_MODE_BARE,
        'setup_list': TEMPLATE_VIEW_MODE_PLAIN,
        'user_list': TEMPLATE_VIEW_MODE_PLAIN,
        'user_add': TEMPLATE_VIEW_MODE_PLAIN,
        'user_edit': TEMPLATE_VIEW_MODE_PLAIN,
        'user_delete': TEMPLATE_VIEW_MODE_PLAIN,
        'user_set_password': TEMPLATE_VIEW_MODE_PLAIN,
        'group_list': TEMPLATE_VIEW_MODE_PLAIN,
        'group_add': TEMPLATE_VIEW_MODE_PLAIN,
        'group_edit': TEMPLATE_VIEW_MODE_PLAIN,
        'group_delete': TEMPLATE_VIEW_MODE_PLAIN,
        'group_members': TEMPLATE_VIEW_MODE_PLAIN,
        
        'role_list': TEMPLATE_VIEW_MODE_PLAIN,
        'role_permissions': TEMPLATE_VIEW_MODE_PLAIN,
        'role_edit': TEMPLATE_VIEW_MODE_PLAIN,
        'role_create': TEMPLATE_VIEW_MODE_PLAIN,
        'role_delete': TEMPLATE_VIEW_MODE_PLAIN,
        'permission_grant_revoke': TEMPLATE_VIEW_MODE_PLAIN,
        'role_members': TEMPLATE_VIEW_MODE_PLAIN,
        
        'menu_list': TEMPLATE_VIEW_MODE_PLAIN,
        'menu_add': TEMPLATE_VIEW_MODE_PLAIN,
        'menu_edit': TEMPLATE_VIEW_MODE_PLAIN,
        'menu_delete': TEMPLATE_VIEW_MODE_PLAIN,

        'url_list': TEMPLATE_VIEW_MODE_PLAIN,
        'url_add': TEMPLATE_VIEW_MODE_PLAIN,
        'url_edit': TEMPLATE_VIEW_MODE_PLAIN,
        'url_delete': TEMPLATE_VIEW_MODE_PLAIN,

        'link_list': TEMPLATE_VIEW_MODE_PLAIN,
        'link_add': TEMPLATE_VIEW_MODE_PLAIN,
        'link_edit': TEMPLATE_VIEW_MODE_PLAIN,
        'link_delete': TEMPLATE_VIEW_MODE_PLAIN,
    }    
}
