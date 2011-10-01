from django.utils.translation import ugettext_lazy as _

MARKUP_TEXTILE = u'textile'
MARKUP_MARKDOWN = u'markdown'
MARKUP_RESTRUCTUREDTEXT = u'rest'

MARKUP_CHOICES = (
    (MARKUP_TEXTILE, _(u'Textile')),
    (MARKUP_MARKDOWN, _(u'Markdown')),
    (MARKUP_RESTRUCTUREDTEXT, _(u'reStructuredText')),
)
