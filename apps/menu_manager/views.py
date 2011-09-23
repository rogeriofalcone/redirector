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

from menu_manager.models import MenuEntry
from menu_manager.forms import MenuEntryForm
from menu_manager import menu_promote as menu_promote_link
from menu_manager import menu_demote as menu_demote_link
from menu_manager import menu_edit as menu_edit_link
from menu_manager import menu_delete as menu_delete_link
from menu_manager import menu_add_child as menu_add_child_links


def menu_list(request, parent_menu_entry_id=None):
#    check_permissions(request.user, [PERMISSION_USER_VIEW])
    if parent_menu_entry_id:
        parent_menu_entry = get_object_or_404(MenuEntry, pk=parent_menu_entry_id)
        title = _(u'menu entries for: %s') % parent_menu_entry
    else:
        parent_menu_entry = None
        title = _(u'root menu entries')
       
    context = {
        'template_id': u'menu_list',
        'title': title,
        'extra_columns': [
            {
                'name': _(u'internal name'),
                'attribute': 'slug'
            },
            {
                'name': _(u'destination'),
                'attribute': 'content_object',
            },
            {
                'name': _(u'enabled'),
                'attribute': encapsulate(lambda x: two_state_template(x.enabled)),
            },
        ],
        'multi_select_as_buttons': True,
        'object': parent_menu_entry,
        'object_name': _(u'menu entry'),
        'navigation_object_links': [menu_promote_link, menu_demote_link, menu_edit_link, menu_delete_link],
    }

    return object_list(
        request,
        queryset=MenuEntry.objects.filter(parent=parent_menu_entry),
        template_name='generic_list.html',
        extra_context=context
    )


def menu_edit(request, menu_entry_id):
    #check_permissions(request.user, [PERMISSION_USER_EDIT])
    menu_entry = get_object_or_404(MenuEntry, pk=menu_entry_id)

    if request.method == 'POST':
        form = MenuEntryForm(instance=menu_entry, data=request.POST)
        if form.is_valid():
            menu_entry = form.save()
            messages.success(request, _(u'Menu entry "%s" updated successfully.') % menu_entry)
            if menu_entry.parent:
                return HttpResponseRedirect(reverse('menu_details', args=[menu_entry.parent.pk]))
            else:
                return HttpResponseRedirect(reverse('menu_list'))            
    else:
        form = MenuEntryForm(instance=menu_entry)

    return render_to_response('generic_form.html', {
        'template_id': u'menu_edit',
        'title': _(u'edit menu entry: %s') % menu_entry,
        'form': form,
        'object': menu_entry,
        'object_name': _(u'menu entry'),
    },
    context_instance=RequestContext(request))


def menu_add(request, parent_menu_entry_id=None):
    #check_permissions(request.user, [PERMISSION_USER_CREATE])

    if parent_menu_entry_id:
        parent_menu_entry = get_object_or_404(MenuEntry, pk=parent_menu_entry_id)
        title = _(u'create new menu entry for: %s') % parent_menu_entry
    else:
        parent_menu_entry = None
        title = _(u'create new root menu entry')

    if request.method == 'POST':
        form = MenuEntryForm(request.POST)
        if form.is_valid():
            menu_entry = form.save(commit=False)
            menu_entry.parent = parent_menu_entry
            menu_entry.save()
            messages.success(request, _(u'Menu entry "%s" created successfully.') % menu_entry)
            if parent_menu_entry:
                return HttpResponseRedirect(reverse('menu_details', args=[parent_menu_entry.pk]))
            else:
                return HttpResponseRedirect(reverse('menu_list'))
    else:
        form = MenuEntryForm()

    return render_to_response('generic_form.html', {
        'template_id': u'menu_add',
        'title': title,
        'form': form,
        'object': parent_menu_entry,
        'object_name': _(u'menu entry'),        
    },
    context_instance=RequestContext(request))


def menu_delete(request, menu_entry_id=None, menu_entry_id_list=None):
    #check_permissions(request.user, [PERMISSION_USER_DELETE])
    post_action_redirect = None

    if menu_entry_id:
        menu_entries = [get_object_or_404(MenuEntry, pk=menu_entry_id)]
        if menu_entries[0].parent:
            post_action_redirect = reverse('menu_details', args=[menu_entries[0].parent.pk])
        else:
            post_action_redirect = reverse('menu_list')
    elif menu_entry_id_list:
        menu_entries = [get_object_or_404(MenuEntry, pk=menu_entry_id) for menu_entry_id in menu_entry_id_list.split(',')]
        if menu_entries[0].parent:
            # This asumes all selected entries are from the same parent
            post_action_redirect = reverse('menu_list', args=[menu_entries[0].parent.pk])
    else:
        messages.error(request, _(u'Must provide at least one menu entry.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for menu_entry in menu_entries:
            try:
                menu_entry.delete()
                messages.success(request, _(u'Menu entry "%s" deleted successfully.') % menu_entry)
            except Exception, e:
                messages.error(request, _(u'Error deleting menu entry "%(menu_entry)s": %(error)s') % {
                    'menu_entry': menu_entry, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'template_id': u'menu_delete',
        'object_name': _(u'menu entry'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'tab_delete.png',
    }
    if len(menu_entries) == 1:
        context['object'] = menu_entries[0]
        context['title'] = _(u'Are you sure you wish to delete the menu entry: %s?') % ', '.join([unicode(d) for d in menu_entries])
    elif len(menu_entries) > 1:
        context['title'] = _(u'Are you sure you wish to delete the menu entries: %s?') % ', '.join([unicode(d) for d in menu_entries])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def menu_multiple_delete(request):
    return menu_delete(
        request, menu_entry_id_list=request.GET.get('id_list', [])
    )


def menu_promote(request, menu_entry_id):
    menu_entry = get_object_or_404(MenuEntry, pk=menu_entry_id)
    menu_entry.promote()
    if menu_entry.parent:
        return HttpResponseRedirect(reverse('menu_details', args=[menu_entry.parent.pk]))
    else:
        return HttpResponseRedirect(reverse('menu_list'))

        
def menu_demote(request, menu_entry_id):
    menu_entry = get_object_or_404(MenuEntry, pk=menu_entry_id)
    menu_entry.demote()
    if menu_entry.parent:
        return HttpResponseRedirect(reverse('menu_details', args=[menu_entry.parent.pk]))
    else:
        return HttpResponseRedirect(reverse('menu_list'))    
