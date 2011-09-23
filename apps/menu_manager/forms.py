from django import forms
from django.utils.translation import ugettext_lazy as _

from menu_manager.models import MenuEntry


class MenuEntryForm(forms.ModelForm):
    class Meta:
        model = MenuEntry
        exclude = ('content_type', 'object_id', 'parent', 'order')
