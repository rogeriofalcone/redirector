from django.conf.urls.defaults import patterns, url
from django.conf import settings

urlpatterns = patterns('webtheme.views',
    url(r'^$', 'home', (), 'home'),
    url(r'^about/$', 'about', (), 'about'),
    url(r'^contact/$', 'contact', (), 'contact'),
)

urlpatterns += patterns('',
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '%s%s' % (settings.STATIC_URL, 'images/favicon.ico')}),
)
