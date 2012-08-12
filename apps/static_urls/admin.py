from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from static_urls.models import URL
   

class URLAdmin(admin.ModelAdmin):
    model = URL
    change_list_template = 'smuggler/change_list.html'
    list_display = ('title', 'url', 'enabled')


admin.site.register(URL, URLAdmin)
