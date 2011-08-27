from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from webtheme.models import SiteSkin
   

class SiteSkinAdmin(admin.ModelAdmin):
    model = SiteSkin
    list_display = ('pk', 'site', 'skin')
    list_display_links = ('pk',)
    list_editable = ('site', 'skin',)
    
admin.site.register(SiteSkin, SiteSkinAdmin)
