from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models import Max

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey


class MenuEntry(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    title = models.CharField(max_length=64, verbose_name=_(u'title'))
    slug = models.SlugField(blank=True, verbose_name=_(u'internal name'))
    description = models.TextField(blank=True, verbose_name=_(u'description'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    order = models.PositiveIntegerField(default=0, verbose_name=_(u'order'))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if not self.pk and not self.order:
            max_order = MenuEntry.objects.filter(parent=self.parent).aggregate(Max('order'))['order__max']
            if max_order:
                self.order = max_order + 1
            else:
                self.order = 1
           
        super(MenuEntry, self).save(*args, **kwargs)

    @property
    def destination(self):
        return self.content_object if self.content_object else _(u'none')        

    def promote(self):
        if self.order > 1:
            siblings = MenuEntry.objects.filter(parent=self.parent)
            if siblings:
                displaced = siblings.get(order=self.order - 1)
                displaced.order += 1
                displaced.save()
                self.order -= 1
                self.save()

    def demote(self):
        siblings = MenuEntry.objects.filter(parent=self.parent)
        if self.order < siblings.count():
            if siblings:
                displaced = siblings.get(order=self.order + 1)
                displaced.order -= 1
                displaced.save()
                self.order += 1
                self.save()

    @models.permalink
    def get_absolute_url(self):
        return ('menu_details', [self.pk])

    class MPTTMeta:
        order_insertion_by=['order']        

    class Meta:
        verbose_name = _(u'menu entry')
        verbose_name_plural = _(u'menu entries')
        ordering = ('order',)
