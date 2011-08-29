from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from navigation.widgets import button_navigation_widget

from project_setup.api import setup_items


def setup_list(request):
    context = {
        'object_list': [button_navigation_widget(request, item) for item in setup_items],
        'title': _(u'setup items'),
        'template_id': u'setup_list'
    }

    return render_to_response('generic_list_horizontal.html', context,
        context_instance=RequestContext(request))
