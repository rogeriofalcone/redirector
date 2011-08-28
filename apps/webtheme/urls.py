from django.conf.urls.defaults import patterns, url
from django.conf import settings

urlpatterns = patterns('webtheme.views',
    url(r'^$', 'home', (), 'home'),
    url(r'^about/$', 'about', (), 'about'),
    url(r'^contact/$', 'contact', (), 'contact'),
    url(r'^favicon\.ico$', 'favicon', (), 'favicon'),
    url(r'^top_redirect/(?P<url>.*)$', 'top_redirect', (), 'top_redirect'),
    url(r'^top_redirect/$', 'top_redirect', (), 'top_redirect'),
)
