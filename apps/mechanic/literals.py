from django.utils.translation import ugettext_lazy as _

ELEMENT_ANCHOR = 'a'
ELEMENT_IMAGE = 'img'
ELEMENT_LINK = 'link'
ELEMENT_SCRIPT = 'script'
ELEMENT_OPTION = 'option'
ELEMENT_FORM = 'form'

ELEMENT_CHOICES = (
    (ELEMENT_ANCHOR, _(u'Anchor')),
    (ELEMENT_FORM, _(u'Form')),
    (ELEMENT_IMAGE, _(u'Image')),
    (ELEMENT_LINK, _(u'Link')),
    (ELEMENT_SCRIPT, _(u'Script')),
    (ELEMENT_OPTION, _(u'Option')),
)

ATTRIBUTE_SOURCE = 'src'
ATTRIBUTE_HREF = 'href'
ATTRIBUTE_CONTENT = 'content'
ATTRIBUTE_TARGET = 'target'
ATTRIBUTE_VALUE = 'value'
ATTRIBUTE_ACTION = 'action'

ATTRIBUTE_CHOICES = (
    (ATTRIBUTE_SOURCE, _(u'Source')),
    (ATTRIBUTE_HREF, _(u'HRef')),
    (ATTRIBUTE_CONTENT, _(u'Content')),
    (ATTRIBUTE_TARGET, _(u'Target')),
    (ATTRIBUTE_VALUE, _(u'Value')),
    (ATTRIBUTE_ACTION, _(u'Action')),
)

COMPARISON_ICONTAINS = 'icontains'
COMPARISON_CONTAINS = 'contains'
COMPARISON_EQUALS = 'equals'

COMPARISON_CHOICES = (
    (COMPARISON_ICONTAINS, _(u'Contains')),
    (COMPARISON_CONTAINS, _(u'Contains (case sensitive)')),
    (COMPARISON_EQUALS, _(u'Equals')),
)

OPERAND_OR = 'or'
OPERAND_AND = 'and'

OPERAND_CHOICES = (
    (OPERAND_OR, _(u'or')),
    (OPERAND_AND, _(u'and'))
)


ACTION_REMOVE = 'remove'
ACTION_REPLACE = 'replace'

ACTION_CHOICES = (
    (ACTION_REMOVE, _(u'Remove')),
    (ACTION_REPLACE, _(u'Replace')),
)
