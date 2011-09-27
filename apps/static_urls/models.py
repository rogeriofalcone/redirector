from django.db import models
from django.utils.translation import ugettext_lazy as _


class URL(models.Model):
    """
    Define an object based URL wrapper
    """
    
    title = models.CharField(max_length=64, verbose_name=_(u'title'))
    description = models.TextField(blank=True, verbose_name=_(u'description'))
    url = models.CharField(max_length=200, verbose_name=_(u'URL'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))
    
    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return self.url

    class Meta:
        verbose_name = _(u'URL')
        verbose_name_plural = _(u'URLs')
        ordering = ['title', 'url']
