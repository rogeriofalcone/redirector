from django.utils.translation import ugettext_lazy as _

SKIN_GREENBOARD = u'greenboard'
SKIN_EDUCATIONAL_SITE = u'educational_site'
SKIN_EDUCATIONAL_SITE_GREEN = u'educational_site_green'
SKIN_GENIO_ESCOLAR = u'genioescolar'

SKIN_CHOICES = (
    (SKIN_GREENBOARD, _(u'TemplateMo.com\'s `green board`')),
    (SKIN_EDUCATIONAL_SITE, _(u'Web-kreation\'s `educational site`')),
    (SKIN_EDUCATIONAL_SITE_GREEN, _(u'Web-kreation\'s `educational site` merged with genio escolar')),
    (SKIN_GENIO_ESCOLAR, _(u'Genio Escolar'))
)

TEMPLATE_VIEW_MODE_FULL = u'full'
TEMPLATE_VIEW_MODE_PLAIN = u'plain'  # No title, footer
TEMPLATE_VIEW_MODE_BARE = u'bare'  # No title, footer, sidebar (for login)
