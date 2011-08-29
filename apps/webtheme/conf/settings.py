"""Configuration options for the web_theme app"""
from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

from webtheme.literals import TEMPLATE_VIEW_MODE_FULL, \
    TEMPLATE_VIEW_MODE_PLAIN

register_settings(
    namespace=u'webtheme',
    module=u'webtheme.conf.settings',
    settings=[
        {'name': u'THEME', 'global_name': u'WEB_THEME_THEME', 'default': u'activo', 'description': _(u'CSS theme to apply, options are: amro, bec, bec-green, blue, default, djime-cerulean, drastic-dark, kathleene, olive, orange, red, reidb-greenish and warehouse.')},
        {'name': u'ENABLE_SCROLL_JS', 'global_name': u'WEB_THEME_ENABLE_SCROLL_JS', 'default': True, 'hidden': True},
        {'name': u'VERBOSE_LOGIN', 'global_name': u'WEB_THEME_VERBOSE_LOGIN', 'default': True, 'description': _(u'Display extra information in the login screen.')},
    ]
)

TEMPLATE_VIEW_MODES = {
    'educational_site': {
        'login': TEMPLATE_VIEW_MODE_PLAIN,
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
    }
}
