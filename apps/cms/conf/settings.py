"""
Configuration options for the CMS app
"""
import hashlib
import uuid
import os

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from storage.backends.filebasedstorage import FileBasedStorage
from smart_settings.api import register_settings

def default_checksum(x):
    """hashlib.sha256(x).hexdigest()"""
    return hashlib.sha256(x).hexdigest()

def default_uuid():
    """unicode(uuid.uuid4())"""
    return unicode(uuid.uuid4())

register_settings(
    namespace=u'cms',
    module=u'cms.conf.settings',
    settings=[
        # Saving
        {'name': u'CHECKSUM_FUNCTION', 'global_name': u'CMS_CHECKSUM_FUNCTION', 'default': default_checksum},
        {'name': u'UUID_FUNCTION', 'global_name': u'CMS_UUID_FUNCTION', 'default': default_uuid},
        # Storage
        {'name': u'STORAGE_BACKEND', 'global_name': u'CMS_STORAGE_BACKEND', 'default': FileBasedStorage},
        # Usage
        {'name': u'PREVIEW_SIZE', 'global_name': u'CMS_PREVIEW_SIZE', 'default': u'640x480'},
        {'name': u'MULTIPAGE_PREVIEW_SIZE', 'global_name': u'CMS_MULTIPAGE_PREVIEW_SIZE', 'default': u'160x120'},
        {'name': u'THUMBNAIL_SIZE', 'global_name': u'CMS_THUMBNAIL_SIZE', 'default': u'50x50'},
        {'name': u'DISPLAY_SIZE', 'global_name': u'CMS_DISPLAY_SIZE', 'default': u'1200'},
        {'name': u'RECENT_COUNT', 'global_name': u'CMS_RECENT_COUNT', 'default': 40, 'description': _(u'Maximum number of recent (created, edited, viewed) media to remember per user.')},
        {'name': u'ZOOM_PERCENT_STEP', 'global_name': u'CMS_ZOOM_PERCENT_STEP', 'default': 50, 'description': _(u'Amount in percent zoom in or out a media file per user interaction.')},
        {'name': u'ZOOM_MAX_LEVEL', 'global_name': u'CMS_ZOOM_MAX_LEVEL', 'default': 200, 'description': _(u'Maximum amount in percent (%) to allow user to zoom in a media file interactively.')},
        {'name': u'ZOOM_MIN_LEVEL', 'global_name': u'CMS_ZOOM_MIN_LEVEL', 'default': 50, 'description': _(u'Minimum amount in percent (%) to allow user to zoom out a media file interactively.')},
        {'name': u'ROTATION_STEP', 'global_name': u'CMS_ROTATION_STEP', 'default': 90, 'description': _(u'Amount in degrees to rotate a media file per user interaction.')},
        #
        {'name': u'CACHE_PATH', 'global_name': u'CMS_CACHE_PATH', 'default': os.path.join(settings.PROJECT_ROOT, 'image_cache'), 'exists': True},
    ]
)
