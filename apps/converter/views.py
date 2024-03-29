from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext

from common.utils import encapsulate
from permissions.api import check_permissions

from converter.api import get_format_list
from converter.conf.settings import GRAPHICS_BACKEND
from converter import CONVERTER_FORMAT_LIST_VIEW


def formats_list(request):
    check_permissions(request.user, [CONVERTER_FORMAT_LIST_VIEW])

    context = {
        'title': _(u'suported file formats'),
        'hide_object': True,
        'object_list': sorted(get_format_list()),
        'extra_columns': [
            {
                'name': _(u'name'),
                'attribute': encapsulate(lambda x: x[0])
            },
            {
                'name': _(u'description'),
                'attribute': encapsulate(lambda x: x[1])
            }
        ],
        'backend': GRAPHICS_BACKEND,
        'template_id': u'crud_list',
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))
