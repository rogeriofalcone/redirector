# Django settings for redirector project.
import os
import sys
from django.core.urlresolvers import reverse
from django.utils.functional import lazy

reverse_lazy = lazy(reverse, str)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), './'))

sys.path.append(os.path.join(PROJECT_ROOT, 'modules'))
sys.path.append(os.path.join(PROJECT_ROOT, 'customization_apps'))
sys.path.append(os.path.join(PROJECT_ROOT, 'apps'))
sys.path.append(os.path.join(PROJECT_ROOT, 'shared_apps'))
sys.path.append(os.path.join(PROJECT_ROOT, '3rd_party_apps'))

PROJECT_TITLE = 'Redirector'
PROJECT_NAME = 'redirector'

DEBUG = False
DEVELOPMENT = False
TEMPLATE_DEBUG = True

ADMINS = ()
SENTRY_ADMINS = ('root@localhost',)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_ROOT, '%s.sqlite' % PROJECT_NAME),     # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Puerto_Rico'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'es'

ugettext = lambda s: s

LANGUAGES = (
    ('es', ugettext('Spanish')),
    ('en', ugettext('English')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = ''
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = ''
STATIC_URL = '/%s-static/' % PROJECT_NAME

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/media/'
#ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/'
#ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'v8on)1wz06s9!e0(yr6)lbaa)l16_75#pm2yg8&nyxp+k1#2me'

# List of callables that know how to import templates from various sources.
#TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.Loader',
##     'django.template.loaders.eggs.Loader',
#)
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'common.middleware.login_required_middleware.LoginRequiredMiddleware',
    'permissions.middleware.permission_denied_middleware.PermissionDeniedMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'converter',
    'mptt',
    'pagination',
    'dynamic_search',
    'permissions',
    'navigation',
    'user_management',
    'project_setup',
    'project_tools',
    'smart_settings',
    'common',
    'mechanic',
    'menu_manager',
    'static_urls',
    'webtheme',
    'markitup',
    'mimetype',
    'storage',
    'cms',
    'main',
    'sentry',
    'sentry.client',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'webtheme.context_processors.current_skin',
    'common.context_processors.current_site',
)

#=================================
SENDFILE_BACKEND = 'sendfile.backends.simple'
GRAPPELLI_ADMIN_TITLE = PROJECT_TITLE
#--------- Django -------------------
LOGIN_URL = reverse_lazy('login_view')  # '/login/'
LOGIN_REDIRECT_URL = reverse_lazy('top_redirect')
#-------- LoginRequiredMiddleware ----------
LOGIN_EXEMPT_URLS = (
    r'^favicon\.ico$',
    r'^about\.html$',
    r'^legal/',  # allow the entire /legal/* subsection
    r'^%s-static/' % PROJECT_NAME,

    r'^accounts/register/$',
    r'^accounts/register/complete/$',
    r'^accounts/register/closed/$',

    r'^accounts/activate/complete/',
    r'^accounts/activate/(?P<activation_key>\w+)/$',

    r'^password/reset/$',
    r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
    r'^password/reset/complete/$',
    r'^password/reset/done/$',
    
    r'^home/$',
    r'^/$',
    r'^$',
    r'^about/$',
    r'^contact/$',
    r'^top_redirect',
)
#--------- Pagination ----------------
PAGINATION_INVALID_PAGE_RAISES_404 = True

try:
    from settings_local import *
except ImportError:
    pass

if DEVELOPMENT:
    INTERNAL_IPS = ('127.0.0.1',)

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )
    try:
        import rosetta
        INSTALLED_APPS += ('rosetta',)
    except ImportError:
        #print 'rosetta is not installed'
        pass

    try:
        import django_extensions
        INSTALLED_APPS += ('django_extensions',)
    except ImportError:
        #print 'django_extensions is not installed'
        pass

    try:
        import debug_toolbar
        #INSTALLED_APPS +=('debug_toolbar',)
    except ImportError:
        #print 'debug_toolbar is not installed'
        pass

    TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.debug',)

    WSGI_AUTO_RELOAD = True
    if 'debug_toolbar' in INSTALLED_APPS:
        MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
        DEBUG_TOOLBAR_CONFIG = {
            'INTERCEPT_REDIRECTS': False,
        }


#from cms.markups import render
MARKITUP_FILTER = ('cms.models.render', {'markup': 'creole'})
