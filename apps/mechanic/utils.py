import re, htmlentitydefs
import binascii
import base64
import time
    
from django.conf import settings
    
##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


def encode_url(url):
    return binascii.hexlify(base64.b64encode(url))


def decode_url(url):
    return base64.b64decode(binascii.unhexlify(url))

 
def print_timing(func):
    def wrapper(*args, **kwargs):
        if settings.DEBUG:
            t1 = time.time()
            res = func(*args, **kwargs)
            t2 = time.time()
            print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        else:
            res = func(*args, **kwargs)
        return res
    return wrapper
 
