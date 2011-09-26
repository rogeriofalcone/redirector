from django import forms
from django.utils.translation import ugettext_lazy as _

from main.models import URL


class URLForm(forms.ModelForm):
    class Meta:
        model = URL
