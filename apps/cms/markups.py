from django.contrib.markup.templatetags.markup import restructuredtext

from cms.literals import MARKUP_MARKDOWN, MARKUP_RESTRUCTUREDTEXT, \
    MARKUP_TEXTILE


def render_rest(content):
    return 'test'

def render(content, markup):
    if markup == MARKUP_RESTRUCTUREDTEXT:
        return restructuredtext(content)
        
    raise NotImplementedError
