from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse

from main.models import CurrentSite


def home(request):
    #import urlparse
    #print urlparse.urlparse(request.build_absolute_uri(request.get_full_path())).hostname
    #print request.get_host()
    #print request.REQUEST.get('page')
    #print request.META.get('PATH_INFO')

    #current_site = config_value('project','CURRENT_SITE')
    
    #print current_site
    
    qs = CurrentSite.objects.filter(selected=True)
    #if 
    skin = 'educational_site'
    #skin = 'greenboard'
    return render_to_response('skins/%s/home.html' % skin, {
        'skin': skin
    }, context_instance=RequestContext(request))


def about(request):
    return render_to_response('about.html', {},
        context_instance=RequestContext(request))

        
def contact(request):
    return render_to_response('about.html', {},
        context_instance=RequestContext(request))
