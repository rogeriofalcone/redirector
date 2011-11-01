from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.text import capfirst

from common.utils import generate_choices_w_labels
from static_urls.models import URL
from mechanic.models import Link
from cms.models import Page

from menu_manager.models import MenuEntry


def convert_to_object(selection):
    model, pk = selection.split(u',')
    ct = ContentType.objects.get(model=model)
    return ct.get_object_for_this_type(pk=pk)

        
def get_destinations():
    pages = Page.objects.filter(enabled=True)
    urls = URL.objects.filter(enabled=True)
    links = Link.objects.filter(enabled=True)
   
    MEDIA_CHOICES = (
        (capfirst(_(u'CMS pages')), generate_choices_w_labels(pages, display_object_type=False),),
        (capfirst(_(u'static links')), generate_choices_w_labels(urls, display_object_type=False),),
        (capfirst(_(u'intercepted links')), generate_choices_w_labels(links, display_object_type=False),),
    )    
    return MEDIA_CHOICES


class MenuEntryForm(forms.ModelForm):
    class Meta:
        model = MenuEntry
        exclude = ('content_type', 'object_id', 'parent', 'order')

    destination = forms.ChoiceField(required=False,
        label=_(u'Destination')
    )

    def __init__(self, *args, **kwargs):
        super(MenuEntryForm, self).__init__(*args, **kwargs)
        self.fields['destination'].choices = get_destinations()

    def clean_destination(self):
        destination = self.cleaned_data['destination']
        if destination:
            return convert_to_object(destination)
        else:
            return None
        #if "fred@example.com" not in data:
        #    raise forms.ValidationError("You have forgotten about Fred!")
