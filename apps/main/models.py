from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey


class CurrentSiteManager(models.Manager):
    def get_current_site(self):
        try:
            return self.get(selected=True).site
        except CurrentSite.DoesNotExist:
            return None
    

class CurrentSite(models.Model):
    site = models.ForeignKey(Site, unique=True, verbose_name=_(u'site'))
    selected = models.BooleanField(verbose_name=_(u'selected'))
    
    objects = CurrentSiteManager()
    
    def __unicode__(self):
        return unicode(self.site)
        
    def save(self, *args, **kwargs):
        if self.selected:
            CurrentSite.objects.update(selected=False)
        super(CurrentSite, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'current site')
        verbose_name_plural = _(u'current site')
        ordering = ['site']
