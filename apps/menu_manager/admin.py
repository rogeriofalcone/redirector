from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mptt.admin import MPTTModelAdmin

from menu_manager.models import MenuEntry

   
class MenuEntryAdmin(MPTTModelAdmin):
    change_list_template = 'smuggler/change_list.html'
    model = MenuEntry
    list_display = ('pk', 'title', 'slug', 'order', 'content_type', 'object_id', 'enabled')
    list_display_links = ('pk',)
    list_editable = ('title', 'slug', 'order', 'enabled')


admin.site.register(MenuEntry, MenuEntryAdmin)
