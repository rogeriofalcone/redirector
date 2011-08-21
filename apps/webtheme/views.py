from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.utils.encoding import smart_unicode


def home(request):
    return render_to_response('home.html', {},
        context_instance=RequestContext(request))

def about(request):
    return render_to_response('about.html', {},
        context_instance=RequestContext(request))
        
def contact(request):
    return render_to_response('about.html', {},
        context_instance=RequestContext(request))        