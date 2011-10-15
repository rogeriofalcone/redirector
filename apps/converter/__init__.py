from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured

from navigation.api import register_sidebar_template
from project_tools.api import register_tool
from permissions.api import register_permission, set_namespace_title

from converter.utils import load_backend
from converter.conf.settings import GRAPHICS_BACKEND

CONVERTER_FORMAT_LIST_VIEW = {'namespace': 'converter', 'name': 'format_list_view', 'label': _(u'View the list of supported file formats.')}

set_namespace_title('converter', _(u'Converter'))
register_permission(CONVERTER_FORMAT_LIST_VIEW)

formats_list = {'text': _('file formats'), 'view': 'formats_list', 'famfam': 'pictures', 'icon': 'pictures.png', 'permissions': [CONVERTER_FORMAT_LIST_VIEW]}

register_sidebar_template(['formats_list'], 'converter_file_formats_help.html')

backend = load_backend().ConverterClass()

register_tool(formats_list)
