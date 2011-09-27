from django import forms
from django.utils.translation import ugettext_lazy as _

from mechanic.models import Link


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
