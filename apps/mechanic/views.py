# -*- coding: utf-8 -*-
import urlparse
import os
import urllib
import posixpath
import re

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.utils.encoding import smart_unicode


import requests
from bs4 import BeautifulSoup
from HTMLParser import HTMLParseError

'''
def resolveComponents(url):
    """
    >>> resolveComponents('http://www.example.com/foo/bar/../../baz/bux/')
    'http://www.example.com/baz/bux/'
    >>> resolveComponents('http://www.example.com/some/path/../file.ext')
    'http://www.example.com/some/file.ext'
    """

    parsed = urlparse.urlparse(url)
    new_path = posixpath.normpath(parsed.path)
    if parsed.path.endswith('/'):
        # Compensate for issue1707768
        new_path += '/'
    cleaned = parsed._replace(path=new_path)
    return cleaned.geturl()


def url_fix(s, charset='utf-8'):
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))
'''

def fix_relative_url(url, parent_url):
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(url)
    if not netloc:
        url = urlparse.urljoin(parent_url, url)
        
    return url


def is_external_top_level_link(url):
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(url)
    if not path or path == '/':
        return True
    else:
        return False


def fetch(request, url):
    r = requests.get(url)
    try:
        soup = BeautifulSoup(r.content)
        for txt in soup.findAll(text=True):
            if re.search('Departamento de Educac', txt, re.I):
                #newtext = 'Barquin International'
                #txt.replaceWith(newtext)
                txt.extract()

            if re.search('proyecto', txt, re.I) and re.search('hogar', txt, re.I):
                newtext = 'Barquin International'
                txt.replaceWith(newtext)

            if (
                    re.search('p r o y', txt, re.I) or
                    re.search('y e c t o', txt, re.I)
                ) and re.search('g a r', txt, re.I):
                newtext = 'B a r q u i n&nbsp;&nbsp;I n t e r n a t i o n a l'
                txt.replaceWith(newtext)

            if re.search('ctor a. garc', txt, re.I):# and txt.parent.name != 'a':
                newtext = 'Barquin International'
                txt.replaceWith(newtext)

        # Convert all images' relative path to an absolute path
        for image in soup.findAll('img'):
            if image.get('src'):
                if re.search('DE_3.JPG', image['src'], re.I) or re.search('pshbanner_ani.gif', image['src'], re.I):
                    image.extract()
                else:
                    image['src'] = fix_relative_url(image['src'], url)

        # Convert links url to absolute and prepend mechanic's url to all links
        for link in soup.findAll('a'):
            if link.get('target'):
                #if link['target'] == '_blank' or link['target'] == '_top':
                if link['target'] != '_self':
                    link['target'] = ''
                
            if link.get('href'):
                if is_external_top_level_link(link['href']) and not link.get('href').startswith('#'):
                    link.extract()
                    #link['href'] = '#'
                    #link.string = 'BLOCKEADO %s BLOCKEADO' % link.string
                elif re.search('www.srh.noaa.gov', link['href'], re.I):
                    link.extract()
                else:
                    href = fix_relative_url(link['href'], url)
                    link['href'] = reverse('fetch', args=[href])
        
        # Convert css links url to absolute and prepend mechanic's url to all links
        for link in soup.findAll('link'):
            if link.get('href'):
                href = fix_relative_url(link['href'], url)

                link['href'] = reverse('fetch', args=[href])    

        content = unicode(soup)#.prettify()
        #content = soup.prettify()
        content_type = None
        #content_type = r.headers['content-type']
    except (HTMLParseError, UnicodeDecodeError, RuntimeError):
        content = r.content
        content_type = r.headers['content-type']
    except AttributeError:
        #print 'url', url
        #print r
        content = 'No content'
        content_type = ''
    #finally:
    
    if r.status_code == requests.codes.NOT_FOUND:
        return render_to_response('http_error_not_found.html', {},
            context_instance=RequestContext(request))
        
    return HttpResponse(
        content=content,
        status=r.status_code,
        content_type=content_type or 'utf-8'
    )
