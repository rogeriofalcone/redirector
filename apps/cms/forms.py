from django import forms
from django.utils.translation import ugettext_lazy as _

from markitup.widgets import MarkItUpWidget

from cms.models import Page

        
class PageForm(forms.ModelForm):
    content = forms.CharField(widget=MarkItUpWidget(
        attrs={'cols': 80, 'rows': 20},
        markitup_set='markitup/sets/wiki'
        )
    )
   
    class Meta:
        model = Page

