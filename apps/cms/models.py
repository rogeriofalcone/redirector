from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from common.utils import shorten_string

from cms.literals import MARKUP_CHOICES, MARKUP_RESTRUCTUREDTEXT
from cms.markups import render


class Page(models.Model):
    enabled = models.BooleanField(verbose_name=_(u'enabled'), default=False)
    title = models.CharField(max_length=200, verbose_name=_(u'title'))
    slug = models.SlugField(blank=True, verbose_name=_(u'internal name'), unique=True)
    description = models.TextField(blank=True, verbose_name=_(u'description'))
    #redirect_to = models.CharField(_('redirect to'), max_length=300, blank=True,
    #    help_text=_('Target URL for automatic redirects.'))
    content = models.TextField(verbose_name=_(u'content'))
    markup = models.CharField(max_length=16, choices=MARKUP_CHOICES, default=MARKUP_RESTRUCTUREDTEXT)
    
    class Meta:
        verbose_name = _(u'CMS page')
        verbose_name_plural = _(u'CMS pages')
        ordering = ('title',)

    def __unicode__(self):
        return self.short_title()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
          
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
       return self.render()
              
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
