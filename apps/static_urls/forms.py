from django import forms
from django.utils.translation import ugettext_lazy as _

from static_urls.models import URL


class URLForm(forms.ModelForm):
    class Meta:
        model = URL
