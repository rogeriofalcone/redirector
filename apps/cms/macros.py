import os
from itertools import chain

from genshi.builder import tag

from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django import forms
from django.forms.util import flatatt
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode


def macro_side_bar_file(macro, environ, *args, **kwargs):
    image = args[0]
    width = args[1]
    caption = args[2]
   
    return tag.div(
        tag.div(
            tag.a(
                tag.img(
                    width=width, class_='thumbimage', src='http://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Herz-Heart.jpg/350px-Herz-Heart.jpg'
                ),
                href='http://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Herz-Heart.jpg/350px-Herz-Heart.jpg', class_='image'
            ),
            tag.div(
                caption, class_='thumbcaption'
            ),            
            style='width:%spx;' % width, class_='thumbinner',
        ),
        class_='thumb tright'
    )

def macro_otheruses(*args, **kwargs):
    return u''


def macro_listen(*args, **kwargs):
    return u''


def macro_reference(*args, **kwargs):
    return u''


def macro_wikitable(*args, **kwargs):
    return u''


def macro_main_article(*args, **kwargs):
    return u''


def macro_listreferences(*args, **kwargs):
    return u''
