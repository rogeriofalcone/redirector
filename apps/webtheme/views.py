from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse

from livesettings import config_value    


def home(request):
    #import urlparse
    #print urlparse.urlparse(request.build_absolute_uri(request.get_full_path())).hostname
    #print request.get_host()
    #print request.REQUEST.get('page')
    #print request.META.get('PATH_INFO')

    current_site = config_value('project','CURRENT_SITE')
    #measurement_system = config_value('project','MEASUREMENT_SYSTEM')
    
    print current_site
    return render_to_response('home.html', {},
        context_instance=RequestContext(request))


def about(request):
    return render_to_response('about.html', {},
        context_instance=RequestContext(request))

        
def contact(request):
    return render_to_response('about.html', {},
        context_instance=RequestContext(request))
