import os
from types import UnicodeType
import hashlib
import uuid
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.markup.templatetags.markup import restructuredtext
from django.core.urlresolvers import reverse
from django.template.defaultfilters import capfirst

import sendfile

from creoleparser import text2html
from creoleparser.dialects import create_dialect, creole10_base, creole11_base
from creoleparser.core import Parser

from common.utils import shorten_string
from common.conf.settings import TEMPORARY_DIRECTORY

from dynamic_search.api import register
from converter.api import convert
from converter.exceptions import UnknownFileFormat, UnkownConvertError
from converter.literals import DEFAULT_ZOOM_LEVEL, DEFAULT_ROTATION, \
    DEFAULT_PAGE_NUMBER

from mimetype.api import get_mimetype, get_icon_file_path, \
    get_error_icon_file_path

from cms.literals import MARKUP_MARKDOWN, MARKUP_RESTRUCTUREDTEXT, \
    MARKUP_TEXTILE, MARKUP_CREOLE, MARKUP_CHOICES
from cms.macros import macro_side_bar_file, macro_otheruses, macro_listen, \
    macro_reference, macro_wikitable, macro_main_article, macro_listreferences
from cms.conf.settings import CHECKSUM_FUNCTION
from cms.conf.settings import UUID_FUNCTION
from cms.conf.settings import STORAGE_BACKEND
from cms.conf.settings import PREVIEW_SIZE
from cms.conf.settings import DISPLAY_SIZE
from cms.conf.settings import CACHE_PATH
    
def internal_link_class(slug):
    try:
        # Have to make two queries, because iexact doesn't understand 
        # unicode, and doesn't match accented lowercase to accented 
        # uppercase characters
        if Page.objects.filter(slug=make_wiki_slug(slug)).filter(enabled=True).count() == 0 and Page.objects.filter(slug=make_wiki_slug(slug, capitalize=True)).filter(enabled=True).count() == 0:
            return 'cms_link_error'
    except Page.DoesNotExist: 
        return 'cms_link_error'


def internal_link_url(slug):
    return reverse('page_render', args=[make_wiki_slug(slug)])

creole_parser = Parser(
    dialect=create_dialect(
        creole11_base,
        wiki_links_path_func=internal_link_url,
        wiki_links_class_func=internal_link_class,
        non_bodied_macros={
            'otrosusos':macro_otheruses,
            'Archivo':macro_side_bar_file,
            'listen':macro_listen,
            'AP':macro_main_article,
            'listaref':macro_listreferences,
        },
        bodied_macros={
            'ref':macro_reference,
            'wikitable':macro_wikitable,
        }
    ),
method='xhtml')


def make_wiki_slug(text, capitalize=False):
    if type(text) != UnicodeType:
        text = unicode(text, 'utf-8', 'ignore')
    
    text = text.replace(u' ', u'_')
    
    if capitalize:
        text = capfirst(text)
    
    return text       


def render(content, markup):        
    if markup == MARKUP_RESTRUCTUREDTEXT:
        return restructuredtext(content)
    elif markup == MARKUP_CREOLE:
        return creole_parser(content)
    
    raise NotImplementedError
        

class Page(models.Model):
    enabled = models.BooleanField(verbose_name=_(u'enabled'), default=False)
    title = models.CharField(max_length=200, verbose_name=_(u'title'), db_index=True)
    slug = models.CharField(max_length=200, blank=True, verbose_name=_(u'internal name'), unique=True, db_index=True)
    description = models.TextField(blank=True, verbose_name=_(u'description'))
    content = models.TextField(verbose_name=_(u'content'))
    markup = models.CharField(max_length=16, choices=MARKUP_CHOICES, default=MARKUP_CREOLE)
    
    class Meta:
        verbose_name = _(u'CMS page')
        verbose_name_plural = _(u'CMS pages')
        ordering = ('title',)

    def __unicode__(self):
        return self.short_title()

    def save(self, *args, **kwargs):
        self.convert_from_wiki()
        if not self.slug:
            self.slug = make_wiki_slug(self.title)
        else:
            self.slug = make_wiki_slug(self.slug)
            
        super(Page, self).save(*args, **kwargs)

    def is_active(self):
        """
        Check whether this page
        """
        if not self.pk:
            return False

        return self.active
    is_active.short_description = _('is active')

    @models.permalink
    def get_absolute_url(self):
       """
       Return the URL to render this page.
       """
       return ('page_render', [self.slug])
                      
    def render(self):
        #render_fn = getattr(self, 'render_%s' % self.region, None)

        #if render_fn:
        #    return render_fn(**kwargs)
        return render(self.content, self.markup)

    def short_title(self):
        """
        Title shortened for display.
        """
        
        return shorten_string(self.title)
    short_title.admin_order_field = 'title'
    short_title.short_description = _('title')

    def convert_from_wiki(self):
        self.content = self.content.replace('\'\'\'\'\'', '**//').replace('\'\'\'', '**').replace('\'\'', '//')
        self.content = self.content.replace('<br />', '\\\\')
        self.content = self.content.replace('{{otrosusos}}', '<<otrosusos>>')
        #self.content = self.content.replace('{{listen', '<<listen')
        #self.content = self.content.replace('}}' '>>')

        
def default_checksum(x):
    """hashlib.sha256(x).hexdigest()"""
    return hashlib.sha256(x).hexdigest()


def default_uuid():
    """unicode(uuid.uuid4())"""
    return unicode(uuid.uuid4())


def get_filename_from_uuid(instance, filename):
    """
    Store the orignal filename of the uploaded file and replace it with
    a UUID
    """
    #filename, extension = os.path.splitext(filename)
    instance.file_filename = filename
    #remove prefix '.'
    #instance.file_extension = extension[1:]
    uuid = UUID_FUNCTION()
    instance.uuid = uuid
    return uuid

# media file cache name hash function
HASH_FUNCTION = lambda x: hashlib.sha256(x).hexdigest()

class Media(models.Model):
    title = models.CharField(max_length=200, verbose_name=_(u'title'))
    slug = models.CharField(max_length=200, blank=True, verbose_name=_(u'internal name'), unique=True)
    description = models.TextField(blank=True, verbose_name=_(u'description'), db_index=True)
    file = models.FileField(upload_to=get_filename_from_uuid, storage=STORAGE_BACKEND(), verbose_name=_(u'file'))
    uuid = models.CharField(max_length=48, default=UUID_FUNCTION(), blank=True, editable=False)
    file_mimetype = models.CharField(max_length=64, default='', editable=False)
    file_mime_encoding = models.CharField(max_length=64, default='', editable=False)
    #FAT filename can be up to 255 using LFN
    file_filename = models.CharField(max_length=255, default=u'', editable=False, db_index=True)
    date_added = models.DateTimeField(verbose_name=_(u'added'), db_index=True, editable=False)
    date_updated = models.DateTimeField(verbose_name=_(u'updated'), db_index=True, editable=False)
    checksum = models.TextField(blank=True, null=True, verbose_name=_(u'checksum'), editable=False)
       
    class Meta:
        verbose_name = _(u'media')
        verbose_name_plural = _(u'media')
        ordering = ('title',)

    def __unicode__(self):
        return self.short_title()

    def save(self, *args, **kwargs):
        """
        Overloaded save method and update the checksum and
        mimetype when originally created
        """
        if not self.slug:
            self.slug = make_wiki_slug(self.title)
        else:
            self.slug = make_wiki_slug(self.slug)
                    
        new_media = not self.pk
        if new_media:
            self.date_added = datetime.now()
            self.date_updated = datetime.now()
        else:
            self.date_updated = datetime.now()
            
        super(Media, self).save(*args, **kwargs)

        if new_media:
            #Only do this for new media
            self.update_checksum(save=False)
            self.update_mimetype(save=False)
            self.save()
        
    def short_title(self):
        """
        Title shortened for display.
        """
        
        return shorten_string(self.title)
    short_title.admin_order_field = 'title'
    short_title.short_description = _('title')        

    #@models.permalink
    #def get_absolute_url(self):
    #    return ('document_view_simple', [self.pk])
    
    def update_mimetype(self, save=True):
        """
        Read a file and determine the mimetype by calling the
        get_mimetype wrapper
        """
        if self.exists():
            try:
                source = open(self.file.path, 'rb')
                mimetype, mime_encoding = get_mimetype(source, self.file_filename)
                if mimetype:
                    self.file_mimetype = mimetype
                else:
                    self.file_mimetype = u''

                if mime_encoding:
                    self.file_mime_encoding = mime_encoding
                else:
                    self.file_mime_encoding = u''
            except:
                self.file_mimetype = u''
                self.file_mime_encoding = u''
            finally:
                if save:
                    self.save()

    def open(self):
        """
        Return a file descriptor to a document's file irrespective of
        the storage backend
        """
        return self.file.storage.open(self.file.path)

    def update_checksum(self, save=True):
        """
        Open a document's file and update the checksum field using the
        user provided checksum function
        """
        if self.exists():
            source = self.open()
            self.checksum = unicode(CHECKSUM_FUNCTION(source.read()))
            source.close()
            if save:
                self.save()

    def exists(self):
        """
        Returns a boolean value that indicates if the document's file
        exists in storage
        """
        return self.file.storage.exists(self.file.path)
        
    def get_cached_image_name(self, page):
        #document_page = self.documentpage_set.get(page_number=page)
        #transformations, warnings = document_page.get_transformation_list()
        transformations = ''
        page = 1
        hash_value = HASH_FUNCTION(u''.join([self.checksum, unicode(page), unicode(transformations)]))
        return os.path.join(CACHE_PATH, hash_value), transformations

    def get_image_cache_name(self, page):
        cache_file_path, transformations = self.get_cached_image_name(page)
        if os.path.exists(cache_file_path):
            return cache_file_path
        else:
            media_file = self.save_to_temp_dir(self.checksum)
            return convert(media_file, output_filepath=cache_file_path, page=page, transformations=transformations)

    def get_image(self, size=DISPLAY_SIZE, page=DEFAULT_PAGE_NUMBER, zoom=DEFAULT_ZOOM_LEVEL, rotation=DEFAULT_ROTATION):
        try:
            image_cache_name = self.get_image_cache_name(page=page)
            return convert(image_cache_name, cleanup_files=False, size=size, zoom=zoom, rotation=rotation)
        except UnknownFileFormat:
            return get_icon_file_path(self.file_mimetype)
        except UnkownConvertError:
            return get_error_icon_file_path()
        except:
            return get_error_icon_file_path()

    def invalidate_cached_image(self, page):
        try:
            os.unlink(self.get_cached_image_name(page)[0])
        except OSError:
            pass
    
    def delete(self, *args, **kwargs):
        super(Media, self).delete(*args, **kwargs)
        return self.file.storage.delete(self.file.path)

    def save_to_file(self, filepath, buffer_size=1024 * 1024):
        """
        Save a copy of the media file from the storage backend
        to the local filesystem
        """
        input_descriptor = self.open()
        output_descriptor = open(filepath, 'wb')
        while True:
            copy_buffer = input_descriptor.read(buffer_size)
            if copy_buffer:
                output_descriptor.write(copy_buffer)
            else:
                break

        output_descriptor.close()
        input_descriptor.close()
        return filepath

    def save_to_temp_dir(self, filename, buffer_size=1024 * 1024):
        temporary_path = os.path.join(TEMPORARY_DIRECTORY, filename)
        return self.save_to_file(temporary_path, buffer_size)
