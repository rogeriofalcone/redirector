from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('mechanic.views',
    url(r'^fetch/(?P<url>.*)$', 'fetch', (), 'fetch'),
)
