from django import forms

from common.forms import DetailForm

from permissions.models import Role


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role


class RoleForm_view(DetailForm):
    class Meta:
        model = Role
