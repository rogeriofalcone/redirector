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

#from user_management import PERMISSION_USER_VIEW, \
#    PERMISSION_USER_EDIT, PERMISSION_USER_CREATE, \
#    PERMISSION_USER_DELETE, PERMISSION_GROUP_CREATE, \
#    PERMISSION_GROUP_EDIT, PERMISSION_GROUP_VIEW, \
#    PERMISSION_GROUP_DELETE
#from user_management.forms import UserForm, PasswordForm, GroupForm

from static_urls.models import URL
from static_urls.forms import URLForm
from static_urls import url_edit as url_edit_link
#from menu_manager import menu_delete as menu_delete_link
#from menu_manager import menu_add_child as menu_add_child_links


def url_list(request):
#    check_permissions(request.user, [PERMISSION_USER_VIEW])
    title = _(u'static link')
       
    context = {
        'template_id': u'url_list',
        'title': title,
        'extra_columns': [
            {
                'name': _(u'URL'),
                'attribute': 'url'
            },
            {
                'name': _(u'enabled'),
                'attribute': encapsulate(lambda x: two_state_template(x.enabled)),
            },
        ],
        'hide_link': True,
        'multi_select_as_buttons': True,
        'navigation_object_links': [url_edit_link],
    }

    return object_list(
        request,
        queryset=URL.objects.all(),
        template_name='generic_list.html',
        extra_context=context
    )


def url_add(request):
    #check_permissions(request.user, [PERMISSION_USER_CREATE])

    title = _(u'create new static link')

    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.save()
            messages.success(request, _(u'Static link "%s" created successfully.') % url)
            return HttpResponseRedirect(reverse('url_list'))
    else:
        form = URLForm()

    return render_to_response('generic_form.html', {
        'template_id': u'url_add',
        'title': title,
        'form': form,
        'object_name': _(u'static link'),        
    },
    context_instance=RequestContext(request))


def url_edit(request, url_id):
    #check_permissions(request.user, [PERMISSION_USER_EDIT])
    url = get_object_or_404(URL, pk=url_id)

    if request.method == 'POST':
        form = URLForm(instance=url, data=request.POST)
        if form.is_valid():
            url = form.save()
            messages.success(request, _(u'Static link "%s" updated successfully.') % url)
            return HttpResponseRedirect(reverse('url_list'))            
    else:
        form = URLForm(instance=url)

    return render_to_response('generic_form.html', {
        'template_id': u'url_edit',
        'title': _(u'edit static link: %s') % url,
        'form': form,
        'object': url,
        'object_name': _(u'static link'),
    },
    context_instance=RequestContext(request))


def url_delete(request, url_id=None, url_id_list=None):
    #check_permissions(request.user, [PERMISSION_USER_DELETE])
    post_action_redirect = None

    if url_id:
        urls = [get_object_or_404(URL, pk=url_id)]
        post_action_redirect = reverse('url_list')
    elif url_id_list:
        urls = [get_object_or_404(URL, pk=url_id) for url_id in url_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one link.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for url in urls:
            try:
                url.delete()
                messages.success(request, _(u'Static link "%s" deleted successfully.') % url)
            except Exception, e:
                messages.error(request, _(u'Error deleting static link "%(url)s": %(error)s') % {
                    'url': url, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'template_id': u'url_delete',
        'object_name': _(u'static link'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'link_delete.png',
    }
    if len(urls) == 1:
        context['object'] = urls[0]
        context['title'] = _(u'Are you sure you wish to delete the static link: %s?') % ', '.join([unicode(d) for d in urls])
    elif len(urls) > 1:
        context['title'] = _(u'Are you sure you wish to delete the static links: %s?') % ', '.join([unicode(d) for d in urls])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def url_multiple_delete(request):
    return url_delete(
        request, url_id_list=request.GET.get('id_list', [])
    )
