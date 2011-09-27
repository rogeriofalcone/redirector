import logging
from urllib2 import HTTPError

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.http import urlencode
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse

from permissions.api import check_permissions
from common.utils import generate_choices_w_labels, encapsulate
from common.widgets import two_state_template
from common.views import assign_remove

from mechanic.api import transform_url
from mechanic.utils import decode_url
from mechanic.models import Link
from mechanic.forms import LinkForm
from mechanic import link_edit as link_edit_link

logger = logging.getLogger(__name__)


def fetch_coded(request, coded_url=None, site_domain=None):
    return fetch(request, decode_url(coded_url), site_domain=site_domain)
    

def fetch(request, url=None, site_domain=None):
    if site_domain:
        site = get_object_or_404(Site, domain=site_domain)
    else:
        site = None
        
    url_query = request.GET
    if url_query:
        url = '%s?%s' % (url, urlencode(url_query))
    logger.debug('fetch(): url: %s' % url)
    try:
        transformed_response = transform_url(url, site)
    except HTTPError:
        #if status_code == requests.codes.NOT_FOUND:
        return render_to_response('http_error_not_found.html', {},
            context_instance=RequestContext(request))
    else:
        return HttpResponse(
            content=transformed_response.get('content', ''),
            status=transformed_response.get('status_code', 200),
            content_type=transformed_response.get('content_type')
        )


def link_list(request):
#    check_permissions(request.user, [PERMISSION_USER_VIEW])
    context = {
        'template_id': u'link_list',
        'title': _(u'intercepted links'),
        'extra_columns': [
            {
                'name': _(u'URL'),
                'attribute': 'url'
            },
            {
                'name': _(u'site'),
                'attribute': 'site'
            },            
            {
                'name': _(u'enabled'),
                'attribute': encapsulate(lambda x: two_state_template(x.enabled)),
            },
        ],
        'multi_select_as_buttons': True,
        'hide_link': True,
        'navigation_object_links': [link_edit_link],
    }

    return object_list(
        request,
        queryset=Link.objects.all(),
        template_name='generic_list.html',
        extra_context=context
    )


def link_add(request):
    #check_permissions(request.user, [PERMISSION_USER_CREATE])

    title = _(u'add new intercepted link')

    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save()
            messages.success(request, _(u'Intercepted link "%s" created successfully.') % link)
            return HttpResponseRedirect(reverse('link_list'))
    else:
        form = LinkForm()

    return render_to_response('generic_form.html', {
        'template_id': u'link_add',
        'title': title,
        'form': form,
        'object_name': _(u'intercepted link'),        
    },
    context_instance=RequestContext(request))


def link_edit(request, link_id):
    #check_permissions(request.user, [PERMISSION_USER_EDIT])
    link = get_object_or_404(Link, pk=link_id)

    if request.method == 'POST':
        form = LinkForm(instance=link, data=request.POST)
        if form.is_valid():
            link = form.save()
            messages.success(request, _(u'Intercepted link "%s" updated successfully.') % link)
            return HttpResponseRedirect(reverse('link_list'))
    else:
        form = LinkForm(instance=link)

    return render_to_response('generic_form.html', {
        'template_id': u'link_edit',
        'title': _(u'edit intercepted link: %s') % link,
        'form': form,
        'object': link,
        'object_name': _(u'intercepted link'),
    },
    context_instance=RequestContext(request))
    
    
def link_delete(request, link_id=None, link_id_list=None):
    #check_permissions(request.user, [PERMISSION_USER_DELETE])
    post_action_redirect = None

    if link_id:
        links = [get_object_or_404(Link, pk=link_id)]
        post_action_redirect = reverse('link_list')
    elif link_id_list:
        links = [get_object_or_404(Link, pk=link_id) for link_id in link_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one link.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for link in links:
            try:
                link.delete()
                messages.success(request, _(u'Intercepted link "%s" deleted successfully.') % link)
            except Exception, e:
                messages.error(request, _(u'Error deleting intercepted link "%(link)s": %(error)s') % {
                    'link': link, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'template_id': u'link_delete',
        'object_name': _(u'intercepted link'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'telephone_link.png',
    }
    if len(links) == 1:
        context['object'] = links[0]
        context['title'] = _(u'Are you sure you wish to delete the intercepted link: %s?') % ', '.join([unicode(d) for d in links])
    elif len(links) > 1:
        context['title'] = _(u'Are you sure you wish to delete the intercepted links: %s?') % ', '.join([unicode(d) for d in links])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def link_multiple_delete(request):
    return link_delete(
        request, link_id_list=request.GET.get('id_list', [])
    )    
