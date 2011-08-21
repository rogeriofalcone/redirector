from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mechanic.models import TransformationRule, POIComparison, \
    ElementComparison


class POIComparisonInline(admin.StackedInline):
    model = POIComparison
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class ElementComparisonInline(admin.StackedInline):
    model = ElementComparison
    extra = 1
    classes = ('collapse-open',)
    allow_add = True
    

class TransformationRuleAdmin(admin.ModelAdmin):
    model = TransformationRule
    radio_fields = {'action': admin.VERTICAL}
    inlines = [
        POIComparisonInline, ElementComparisonInline
    ]

'''
    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        (_(u'Point of origin'), {
            #'classes': ('collapse',),
            'fields': ('point_of_origin', ('point_of_origin_comparison', 'point_of_origin_comparison_negate'))
        }),
        (_(u'Element'), {
            'fields': ('element', ('attribute', 'attribute_comparison', 'negate'), 'value')
        }),        
        (_(u'Action'), {
            'fields': ('action', 'action_argument',)
        }),        
    )
'''    
    
admin.site.register(TransformationRule, TransformationRuleAdmin)
