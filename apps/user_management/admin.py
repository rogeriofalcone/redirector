from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, GroupAdmin as DjangoGroupAdmin


class UserAdmin(DjangoUserAdmin):
    change_list_template = 'smuggler/change_list.html'


class GroupAdmin(DjangoGroupAdmin):
    change_list_template = 'smuggler/change_list.html'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
