from types import UnicodeType

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.markup.templatetags.markup import restructuredtext
from django.core.urlresolvers import reverse
from django.template.defaultfilters import capfirst

from creoleparser import text2html
from creoleparser.dialects import create_dialect, creole10_base, creole11_base
from creoleparser.core import Parser

from common.utils import shorten_string

from cms.literals import MARKUP_MARKDOWN, MARKUP_RESTRUCTUREDTEXT, \
    MARKUP_TEXTILE, MARKUP_CREOLE, MARKUP_CHOICES
from cms.macros import macro_side_bar_file, macro_otheruses, macro_listen, \
    macro_reference, macro_wikitable, macro_main_article, macro_listreferences

    
def internal_link_class(slug):
    try:
        if Page.objects.filter(slug=make_wiki_slug(slug)).filter(enabled=True).count() == 0:
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


def make_wiki_slug(text):
    if type(text) != UnicodeType:
        text = unicode(text, 'utf-8', 'ignore')
        
    text = capfirst(text.replace(u' ', u'_'))
    
    return text       


def render(content, markup):        
    if markup == MARKUP_RESTRUCTUREDTEXT:
        return restructuredtext(content)
    elif markup == MARKUP_CREOLE:
        return creole_parser(content)
    
    raise NotImplementedError
        

class Page(models.Model):
    enabled = models.BooleanField(verbose_name=_(u'enabled'), default=False)
    title = models.CharField(max_length=200, verbose_name=_(u'title'))
    slug = models.CharField(max_length=200, blank=True, verbose_name=_(u'internal name'), unique=True)
    description = models.TextField(blank=True, verbose_name=_(u'description'))
    #redirect_to = models.CharField(_('redirect to'), max_length=300, blank=True,
    #    help_text=_('Target URL for automatic redirects.'))
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
