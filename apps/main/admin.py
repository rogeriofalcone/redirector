from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from main.models import CurrentSite
   

class CurrentSiteAdmin(admin.ModelAdmin):
    model = CurrentSite
    list_display = ('pk', 'site', 'selected')
    list_display_links = ('pk',)
    list_editable = ('site', 'selected',)
    
admin.site.register(CurrentSite, CurrentSiteAdmin)
