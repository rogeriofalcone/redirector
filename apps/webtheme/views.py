from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings

from webtheme.models import SiteSkin


def home(request):
    skin = SiteSkin.objects.get_current_skin()
    return render_to_response('skins/%s/home.html' % skin, {
    }, context_instance=RequestContext(request))


def about(request):
    skin = SiteSkin.objects.get_current_skin()
    return render_to_response('skins/%s/about.html' % skin, {
    }, context_instance=RequestContext(request))

        
def contact(request):
    skin = SiteSkin.objects.get_current_skin()
    return render_to_response('skins/%s/about.html' % skin, {},
        context_instance=RequestContext(request))

       
def favicon(request):
    skin = SiteSkin.objects.get_current_skin()
    return HttpResponseRedirect('%sskins/%s/images/favicon.ico' % (settings.STATIC_URL, skin))
    

def top_redirect(request, url='/'):
    return render_to_response('top_redirect.html', {'url': '/'},
        context_instance=RequestContext(request))
    
    
    
