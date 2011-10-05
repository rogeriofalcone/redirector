from django import forms
from django.utils.translation import ugettext_lazy as _

from markitup.widgets import MarkItUpWidget

from cms.models import Page


class PageForm_create(forms.ModelForm):
    #content = forms.CharField(widget=MarkItUpWidget(
    #    attrs={'cols': 80, 'rows': 20},
    #    markitup_set='markitup/sets/wiki'
    #    )
    #)
   
    class Meta:
        model = Page
        exclude = ('content',)


        
class PageForm_edit(forms.ModelForm):
    #content = forms.CharField(widget=MarkItUpWidget(
    #    attrs={'cols': 80, 'rows': 20},
    #    markitup_set='markitup/sets/wiki'
    #    )
    #)
    def __init__(self, *args, **kwargs):
        super(PageForm_edit, self).__init__(*args, **kwargs)
        self.fields['content'].widget= MarkItUpWidget(
            attrs={'cols': 80, 'rows': 20},
            markitup_set='markitup/sets/creole'
        )
   
    class Meta:
        model = Page
        exclude = ('markup',)

