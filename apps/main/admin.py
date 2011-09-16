from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mptt.admin import MPTTModelAdmin

from main.models import CurrentSite, URL, Tree
   

class CurrentSiteAdmin(admin.ModelAdmin):
    model = CurrentSite
    list_display = ('pk', 'site', 'selected')
    list_display_links = ('pk',)
    list_editable = ('site', 'selected',)
    
    
class URLAdmin(admin.ModelAdmin):
    model = URL
    list_display = ('title', 'url', 'enabled')
    #list_display_links = ('pk',)
    #list_editable = ('site', 'selected',)
    
    
class TreeAdmin(MPTTModelAdmin):
    model = Tree
    list_display = ('pk', 'title', 'slug', 'order', 'content_type', 'object_id', 'enabled')
    list_display_links = ('pk',)
    list_editable = ('title', 'slug', 'order', 'enabled')


admin.site.register(CurrentSite, CurrentSiteAdmin)
admin.site.register(URL, URLAdmin)
admin.site.register(Tree, TreeAdmin)
