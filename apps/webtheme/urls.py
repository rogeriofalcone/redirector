from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('webtheme.views',
    url(r'^$', 'home', (), 'home'),
    url(r'^about/$', 'about', (), 'about'),
    url(r'^contact/$', 'contact', (), 'contact'),
)
