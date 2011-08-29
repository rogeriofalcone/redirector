from django.utils.translation import ugettext_lazy as _

SKIN_GREENBOARD = u'greenboard'
SKIN_EDUCATIONAL_SITE = u'educational_site'

SKIN_CHOICES = (
    (SKIN_GREENBOARD, _(u'TemplateMo.com\'s `green board`')),
    (SKIN_EDUCATIONAL_SITE, _(u'Web-kreation\'s `educational site`'))
)

TEMPLATE_VIEW_MODE_FULL = u'full'
TEMPLATE_VIEW_MODE_PLAIN = u'plain'
