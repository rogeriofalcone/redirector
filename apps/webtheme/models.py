from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site

from webtheme.literals import SKIN_CHOICES


class SiteSkin(models.Model):
    site = models.ForeignKey(Site, unique=True, verbose_name=_(u'site'))
    skin = models.CharField(choices=SKIN_CHOICES, max_length=24, verbose_name=_(u'skin'))
    
    def __unicode__(self):
        return unicode(self.site)

    class Meta:
        verbose_name = _(u'site skin')
        verbose_name_plural = _(u'site skins')
        ordering = ['site']
