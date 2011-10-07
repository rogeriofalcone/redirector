from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse
from django.template.defaultfilters import capfirst
 
import sendfile

from permissions.api import check_permissions
from common.utils import generate_choices_w_labels, encapsulate
from common.widgets import two_state_template
from common.views import assign_remove

from cms.models import Page, Media, make_wiki_slug
from cms.forms import PageForm_create, PageForm_edit, MediaForm
from cms import page_edit_link, page_preview_link, page_render_link
from cms import media_edit_link
from cms.widgets import media_thumbnail
from cms.conf.settings import PREVIEW_SIZE


def page_list(request):
#    check_permissions(request.user, [PERMISSION_USER_VIEW])
    context = {
        'template_id': u'crud_list',
        'title': _(u'CMS pages'),
        'extra_columns': [
            {
                'name': _(u'title'),
                'attribute': 'title'
            },            
            {
                'name': _(u'name'),
                'attribute': 'slug'
            },
            {
                'name': _(u'enabled'),
                'attribute': encapsulate(lambda x: two_state_template(x.enabled)),
            },
        ],
        'multi_select_as_buttons': True,
        'hide_object': True,
        'navigation_object_links': [page_edit_link, page_preview_link, page_render_link],
    }

    return object_list(
        request,
        queryset=Page.objects.all(),
        template_name='generic_list.html',
        extra_context=context
    )

def page_add(request):
    #check_permissions(request.user, [PERMISSION_USER_CREATE])

    title = _(u'add new CMS page')

    if request.method == 'POST':
        form = PageForm_create(request.POST)
        if form.is_valid():
            page = form.save()
            messages.success(request, _(u'CMS page "%s" created successfully.') % page)
            #return HttpResponseRedirect(reverse('page_list'))
            return HttpResponseRedirect(reverse('page_edit', args=[page.pk]))
    else:
        form = PageForm_create()

    return render_to_response('generic_form.html', {
        'template_id': u'crud_add',
        'title': title,
        'form': form,
        'object_name': _(u'CMS page'),        
    },
    context_instance=RequestContext(request))


def page_edit(request, page_id):
    #check_permissions(request.user, [PERMISSION_USER_EDIT])
    page = get_object_or_404(Page, pk=page_id)

    if request.method == 'POST':
        form = PageForm_edit(instance=page, data=request.POST)
        if form.is_valid():
            page = form.save()
            messages.success(request, _(u'CMS page "%s" updated successfully.') % page)
            return HttpResponseRedirect(reverse('page_list'))
    else:
        form = PageForm_edit(instance=page)

    return render_to_response('generic_form.html', {
        'template_id': u'crud_edit',
        'title': _(u'edit CMS page: %s') % page,
        'form': form,
        'object': page,
        'object_name': _(u'CMS page'),
    },
    context_instance=RequestContext(request))
    

def page_delete(request, page_id=None, page_id_list=None):
    #check_permissions(request.user, [PERMISSION_USER_DELETE])
    post_action_redirect = None

    if page_id:
        pages = [get_object_or_404(Page, pk=page_id)]
        post_action_redirect = reverse('page_list')
    elif page_id_list:
        pages = [get_object_or_404(Page, pk=page_id) for page_id in page_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one page.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for page in pages:
            try:
                page.delete()
                messages.success(request, _(u'CMS page "%s" deleted successfully.') % page)
            except Exception, e:
                messages.error(request, _(u'Error deleting CMS page "%(page)s": %(error)s') % {
                    'page': page, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'template_id': u'crud_delete',
        'object_name': _(u'CMS page'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'page_delete.png',
    }
    if len(pages) == 1:
        context['object'] = pages[0]
        context['title'] = _(u'Are you sure you wish to delete the CMS page: %s?') % ', '.join([unicode(d) for d in pages])
    elif len(pages) > 1:
        context['title'] = _(u'Are you sure you wish to delete the CMS pages: %s?') % ', '.join([unicode(d) for d in pages])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def page_multiple_delete(request):
    return page_delete(
        request, page_id_list=request.GET.get('id_list', [])
    )


def page_view(request, page_id=None, slug=None, preview=True):
    #check_permissions(request.user, [PERMISSION_USER_EDIT])
    if page_id:
        page = get_object_or_404(Page, pk=page_id)
    elif slug:
        page = get_object_or_404(Page, slug=capfirst(slug))
    else:
        raise Http404

    context = {
        'template_id': u'crud_view',
        'title': page.title,
        'content': page.render(),
    }
    
    if not preview:
        context['template_id'] = u'cms_render'
    
    if preview:
        context.update({
            'object': page,
            'object_name': _(u'CMS page'),
            })

    return render_to_response('generic_template.html', context,
        context_instance=RequestContext(request))


def media_list(request):
#    check_permissions(request.user, [PERMISSION_USER_VIEW])
    context = {
        'template_id': u'crud_list',
        'title': _(u'CMS media'),
        'extra_columns': [
            {
                'name': _(u'title'),
                'attribute': 'title'
            },            
            {
                'name': _(u'name'),
                'attribute': 'slug'
            },
            {'name':_(u'thumbnail'), 'attribute':
                encapsulate(lambda x: media_thumbnail(x))
            },
            {
                'name': _(u'mimetype'),
                'attribute': 'file_mimetype'
            },
            #{
            #    'name': _(u'checksum'),
            #    'attribute': 'checksum'
            #},            #{
            #    'name': _(u'enabled'),
            #    'attribute': encapsulate(lambda x: two_state_template(x.enabled)),
            #},
        ],
        'multi_select_as_buttons': True,
        'hide_object': True,
        'navigation_object_links': [media_edit_link],
    }

    return object_list(
        request,
        queryset=Media.objects.all(),
        template_name='generic_list.html',
        extra_context=context
    )

    
def media_add(request):
    #check_permissions(request.user, [PERMISSION_USER_CREATE])

    title = _(u'add new CMS media')

    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save()
            messages.success(request, _(u'CMS media "%s" created successfully.') % media)
            return HttpResponseRedirect(reverse('media_list'))
            #return HttpResponseRedirect(reverse('media_edit', args=[media.pk]))
    else:
        form = MediaForm()

    return render_to_response('generic_form.html', {
        'template_id': u'crud_add',
        'title': title,
        'form': form,
        'object_name': _(u'CMS media'),        
    },
    context_instance=RequestContext(request))


def media_edit(request, media_id):
    #check_permissions(request.user, [PERMISSION_USER_EDIT])
    media = get_object_or_404(Media, pk=media_id)

    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES, instance=media)
        if form.is_valid():
            media = form.save()
            messages.success(request, _(u'CMS media "%s" updated successfully.') % media)
            return HttpResponseRedirect(reverse('media_list'))
    else:
        form = MediaForm(instance=media)

    return render_to_response('generic_form.html', {
        'template_id': u'crud_edit',
        'title': _(u'edit CMS media: %s') % media,
        'form': form,
        'object': media,
        'object_name': _(u'CMS media'),
    },
    context_instance=RequestContext(request))


def media_delete(request, media_id=None, media_id_list=None):
    #check_permissions(request.user, [PERMISSION_USER_DELETE])
    post_action_redirect = None

    if media_id:
        medias = [get_object_or_404(Media, pk=media_id)]
        post_action_redirect = reverse('media_list')
    elif media_id_list:
        medias = [get_object_or_404(Media, pk=media_id) for media_id in media_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one media.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for media in medias:
            try:
                media.delete()
                messages.success(request, _(u'CMS media "%s" deleted successfully.') % media)
            except Exception, e:
                messages.error(request, _(u'Error deleting CMS media "%(media)s": %(error)s') % {
                    'media': media, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'template_id': u'crud_delete',
        'object_name': _(u'CMS media'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'drive_delete.png',
    }
    if len(medias) == 1:
        context['object'] = medias[0]
        context['title'] = _(u'Are you sure you wish to delete the CMS media: %s?') % ', '.join([unicode(d) for d in medias])
    elif len(medias) > 1:
        context['title'] = _(u'Are you sure you wish to delete the CMS media: %s?') % ', '.join([unicode(d) for d in medias])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def media_multiple_delete(request):
    return media_delete(
        request, media_id_list=request.GET.get('id_list', [])
    )


def get_media_image(request, media_id=None, media_name=None, size=PREVIEW_SIZE):
    #check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])
    if media_id:
        media = get_object_or_404(Media, pk=media_id)
    elif media_name:
        media = get_object_or_404(Media, slug=make_wiki_slug(media_name))
        
    #page = int(request.GET.get('page', DEFAULT_PAGE_NUMBER))
    #zoom = int(request.GET.get('zoom', DEFAULT_ZOOM_LEVEL))

    #if zoom < ZOOM_MIN_LEVEL:
    #    zoom = ZOOM_MIN_LEVEL

    #if zoom > ZOOM_MAX_LEVEL:
    #    zoom = ZOOM_MAX_LEVEL

    #rotation = int(request.GET.get('rotation', DEFAULT_ROTATION)) % 360

    return sendfile.sendfile(request, media.get_image(size=size))#, page=page, zoom=zoom, rotation=rotation))
