from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site


class CurrentSite(models.Model):
    site = models.ForeignKey(Site, unique=True, verbose_name=_(u'site'))
    selected = models.BooleanField(verbose_name=_(u'selected'))
    
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