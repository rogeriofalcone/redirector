from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_multi_item_links
from permissions.api import register_permission, set_namespace_title
from project_setup.api import register_setup

from main.models import URL

url_setup = {'text': _(u'URLs'), 'view': 'url_list', 'icon': 'link.png'}#, 'permissions': [PERMISSION_USER_VIEW]}
url_list = {'text': _(u'URL list'), 'view': 'url_list', 'famfam': 'link'}#, 'permissions': [PERMISSION_USER_VIEW]}
url_add = {'text': _(u'new URL'), 'view': 'url_add', 'famfam': 'link_add'}#, 'permissions': [PERMISSION_USER_CREATE]}
url_edit = {'text': _(u'edit'), 'view': 'url_edit', 'args': 'object.id', 'famfam': 'link_edit'}#, 'permissions': [PERMISSION_USER_EDIT]}
url_delete = {u'text': _('delete'), 'view': 'url_delete', 'args': 'object.id', 'famfam': 'link_delete'}#, 'permissions': [PERMISSION_USER_DELETE]}
url_multiple_delete = {u'text': _('delete'), 'view': 'url_multiple_delete', 'famfam': 'link_delete'}#, 'permissions': [PERMISSION_USER_DELETE]}


register_links(URL, [url_edit, url_delete])
register_links(['url_list', 'url_add', 'url_edit', 'url_delete', 'url_multiple_delete'], [url_list, url_add], menu_name=u'sidebar')
register_multi_item_links(['url_list'], [url_multiple_delete])

register_setup(url_setup)


__version_info__ = {
    'major': 0,
    'minor': 35,
    'micro': 0,
    'releaselevel': 'final',
    'serial': 0
}

def get_version():
    """
    Return the formatted version information
    """
    vers = ["%(major)i.%(minor)i" % __version_info__, ]

    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final':
        vers.append('%(releaselevel)s%(serial)i' % __version_info__)
    return ''.join(vers)

__version__ = get_version()
