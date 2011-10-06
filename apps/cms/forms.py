from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from markitup.widgets import MarkItUpWidget
#from markitup import settings as markitup_settings

from cms.models import Page, Media


class PageForm_create(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PageForm_create, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs={'cols': 80, 'rows': 2}
               
    class Meta:
        model = Page
        exclude = ('content',)


        
class PageForm_edit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PageForm_edit, self).__init__(*args, **kwargs)
        self.fields['content'].widget= MarkItUpWidget(
            attrs={'cols': 80, 'rows': 20},
            markitup_set='markitup/sets/%s' % self.instance.markup
        )
        self.fields['description'].widget.attrs={'cols': 80, 'rows': 2}

    class Meta:
        model = Page
        exclude = ('markup',)


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
