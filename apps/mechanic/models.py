from django.db import models
from django.utils.translation import ugettext_lazy as _

from mechanic.literals import ELEMENT_CHOICES, ATTRIBUTE_CHOICES, \
    COMPARISON_CHOICES, ACTION_CHOICES, OPERAND_CHOICES, OPERAND_AND
    

class TransformationRule(models.Model):
    """
    Define the criteria by which each element of a page is evaluated
    """

    title = models.CharField(max_length=64, verbose_name=_(u'title'))
    description = models.TextField(blank=True, verbose_name=_(u'description'))
    point_of_origin = models.CharField(max_length=200, blank=True, verbose_name=_(u'point of origin'))
    element = models.CharField(max_length=16, blank=True, choices=ELEMENT_CHOICES, verbose_name=_(u'element'))
    attribute = models.CharField(max_length=16, choices=ATTRIBUTE_CHOICES, verbose_name=_(u'attribute'))
    action = models.CharField(max_length=16, choices=ACTION_CHOICES, verbose_name=_(u'action'))
    action_argument = models.TextField(blank=True, verbose_name=_(u'action argument'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'transformation rule')
        verbose_name_plural = _(u'transformation rules')
        ordering = ['title']


class POIComparison(models.Model):
    transformation_rule = models.ForeignKey(TransformationRule, verbose_name=_(u'transformation rule'))
    point_of_origin_comparison_operand = models.CharField(max_length=8, default=OPERAND_AND, choices=OPERAND_CHOICES, verbose_name=_(u'operand'))
    point_of_origin_comparison = models.CharField(max_length=16, choices=COMPARISON_CHOICES, verbose_name=_(u'point of origin comparison'))
    point_of_origin_comparison_negate = models.BooleanField(verbose_name=_(u'negate'), help_text=_(u'Inverts the point of origin comparison.'))

    def __unicode__(self):
        return '%s - %s - [%s]' % (self.point_of_origin_comparison_operand, self.point_of_origin_comparison, u'X' if self.point_of_origin_comparison_negate else u' ')

    class Meta:
        verbose_name = ''  #_(u'point of origin comparison')
        verbose_name_plural = _(u'point of origin comparisons')


class ElementComparison(models.Model):
    transformation_rule = models.ForeignKey(TransformationRule, verbose_name=_(u'transformation rule'))
    attribute_comparison_operand = models.CharField(max_length=8, default=OPERAND_AND, choices=OPERAND_CHOICES, verbose_name=_(u'operand'))
    attribute_comparison = models.CharField(max_length=16, choices=COMPARISON_CHOICES, verbose_name=_(u'attribute comparison'))
    negate = models.BooleanField(verbose_name=_(u'negate'), help_text=_(u'Inverts the attribute comparison.'))
    value = models.TextField(blank=True, verbose_name=_(u'value'))

    def __unicode__(self):
        return '%s: %s [%s] %s: "%s" ' % (
            self.attribute_comparison_operand,
            self.transformation_rule.attribute,
            _(u'not') if self.negate else u' ',
            self.attribute_comparison,
            self.value,
        )

    class Meta:
        verbose_name = ''  #_(u'element comparison')
        verbose_name_plural = _(u'element comparisons')
