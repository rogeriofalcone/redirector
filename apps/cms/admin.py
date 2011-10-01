from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from cms.models import Page

   
class PageAdmin(admin.ModelAdmin):
    model = Page
    #list_display = ('pk', 'title', 'slug', 'order', 'content_type', 'object_id', 'enabled')
    #list_display_links = ('pk',)
    #list_editable = ('title', 'slug', 'order', 'enabled')


admin.site.register(Page, PageAdmin)
