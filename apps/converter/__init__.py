from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured

from navigation.api import register_sidebar_template
from project_tools.api import register_tool

from converter.utils import load_backend
from converter.conf.settings import GRAPHICS_BACKEND

formats_list = {'text': _('file formats'), 'view': 'formats_list', 'famfam': 'pictures', 'icon': 'pictures.png'}

register_sidebar_template(['formats_list'], 'converter_file_formats_help.html')

backend = load_backend().ConverterClass()

register_tool(formats_list)
