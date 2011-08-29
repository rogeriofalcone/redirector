from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^mechanic/', include('mechanic.urls')),
    (r'^smart_settings/', include('smart_settings.urls')),
    (r'^user_management/', include('user_management.urls')),
    (r'^project_setup/', include('project_setup.urls')),
    (r'^permissions/', include('permissions.urls')),
    (r'^', include('webtheme.urls')),
    (r'^', include('common.urls')),
    (r'^sentry/', include('sentry.web.urls')),
)

if settings.DEVELOPMENT:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

    if 'rosetta' in settings.INSTALLED_APPS:
        urlpatterns += patterns('',
            url(r'^rosetta/', include('rosetta.urls'), name='rosetta'),
        )
