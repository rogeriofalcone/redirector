import urlparse
import logging
    
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode, force_unicode, smart_str, DjangoUnicodeDecodeError
from django.db.models import Q

import mechanize
from bs4 import BeautifulSoup, UnicodeDammit
import requests
from HTMLParser import HTMLParseError

from mechanic.literals import ATTRIBUTE_CONTENT, OPERAND_OR, \
    OPERAND_AND, ACTION_REMOVE, ACTION_REPLACE
from mechanic.models import TransformationRule
from mechanic.utils import unescape, encode_url, print_timing
from mechanic.comparisons import COMPARISON_FUNCTIONS

logger = logging.getLogger(__name__)

USE_MECHANIZE = True
ENCODE_URLS = False


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


def compare_elements(elements, element_comparison, rule_dictionary, attribute=None):
    results = []
    for element in elements:
        if rule_dictionary.get('text', False):
            # Compare the element contents (text)
            s2 = element
        else:
            # Compare an attribute of the element
            attribute_value = element.get(attribute)
            s2 = attribute_value
        
        if s2:
            if COMPARISON_FUNCTIONS[element_comparison.attribute_comparison](element_comparison.value, s2):
                results.append(element)
            

    return set(results)


@print_timing
def fix_links(soup, url, site=None):
    # Convert all images' relative path to an absolute path
    for image in soup.findAll('img'):
        if image.get('src'):
            image['src'] = fix_relative_url(image['src'], url)

    # Convert links url to absolute url
    for link in soup.findAll('a'):
        if link.get('href'):
            if is_external_top_level_link(link['href']) and not link.get('href').startswith('#'):
                pass
            else:
                link['href'] = fix_relative_url(link['href'], url)

    # Convert css links url to absolute url
    for link in soup.findAll('link'):
        if link.get('href'):
            link['href'] = fix_relative_url(link['href'], url)
            
    # Convert scripts links url to absolute url
    for script in soup.findAll('script'):
        if script.get('src'):
            script['src'] = fix_relative_url(script['src'], url)
    
    return soup

    
@print_timing
def transform_soup(soup, url, site=None):
    for rule in TransformationRule.objects.filter(Q(enabled=True) & (Q(sites=None) | Q(sites=site))):
        rule_dictionary = {}
        source_attribute = None

        if rule.element:
            rule_dictionary['name'] = rule.element

        if rule.attribute == ATTRIBUTE_CONTENT:
            rule_dictionary['text'] = True
        else:
            if rule.attribute:
                source_attribute = rule.attribute

        # Find elements of rule
        elements = soup.findAll(**rule_dictionary)
        element_comparison_result = None
        
        # Compare elements of rule
        for element_comparison in rule.elementcomparison_set.all():
            results = compare_elements(elements, element_comparison, rule_dictionary, source_attribute)
            if element_comparison_result is None:
                element_comparison_result = results
            else:
                if element_comparison.attribute_comparison_operand == OPERAND_AND:
                    element_comparison_result &= results
                else:
                    element_comparison_result |= results

        # Execute action of rule
        for result_element in list(element_comparison_result):
            if rule.action == ACTION_REMOVE:
                parent = result_element.parent
                result_element.extract()
                if rule.parent_count:
                    try:
                        tag = result_element.parent
                        for current in range(rule.parent_count):
                            grand_father = parent.parent
                            parent.extract()
                            parent = grand_father
                    except Exception, err:
                        logger.error('transform_url(): Parent removal error: %s' % err)
                        
            elif rule.action == ACTION_REPLACE:
                try:
                    code = compile(u'code_result=%s' % unicode(rule.action_argument), '<string>', 'exec')
                    if rule.attribute == ATTRIBUTE_CONTENT:
                        ns = {
                            'source': result_element,
                            'site': site,
                            'reverse': reverse,
                        }
                        exec code in ns
                        result_element.replaceWith(ns['code_result'])
                    else:
                        ns = {
                            'source': result_element[rule.attribute],
                            'site': site,
                            'reverse': reverse,
                        }
                        exec code in ns
                        result_element[rule.attribute] = ns['code_result']
                except Exception, err:
                    raise Exception('Error handling rule: "%s"; error: %s' % (rule, err))
    
    return soup   
    
    
@print_timing
def retrieve_html(url):
    if USE_MECHANIZE:
        br = mechanize.Browser(factory=mechanize.RobustFactory())
        response = br.open(url)
        status_code = response._headers.status
        content = response.read()
        content_type = response._headers.typeheader
    else:
        transformed_response = {}
        response = requests.get(url, allow_redirects=True)
        status_code = response.status_code
        content = response.content
        content_type = response.headers['content-type']
        
    return {
        'content': content,
        'content_type': content_type,
        'status_code': status_code,
        'response': response,
    }
    

@print_timing
def transform_url(url, site):
    transformed_response = {}
    
    original_response = retrieve_html(url)
    
    if not USE_MECHANIZE:
        original_response['response'].raise_for_status()        

    if 'text' in original_response['content_type']:
        try:
            #html = unescape(html)
            #html = unicode(BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES))
            html = original_response['content']
            try:
                html = smart_unicode(html)
            except DjangoUnicodeDecodeError:
                pass
                
            soup = BeautifulSoup(html)
            
            #, smartQuotesTo=None)
            #, fromEncoding="windows-1252")

            soup = fix_links(soup, url, site)
            soup = transform_soup(soup, url, site)
            soup = intercept_links(soup, url, encode=ENCODE_URLS, site=site)
            
            #transformed_response['content'] = soup.prettify()
            transformed_response['content'] = unicode(soup)

        #except (HTMLParseError, UnicodeDecodeError, RuntimeError), err:
        except (HTMLParseError, RuntimeError), err:
            logger.error('transform_url(): HTMLParseError, or RuntimeError; %s' % url)
            
            transformed_response['content'] = original_response['content']
            transformed_response['content_type'] = original_response['content_type']

        #except Exception, err:
        #    logger.debug('transform_url(): Unhandled exception: %s' % err)
        #    transformed_response['content'] = response.read()
        #    transformed_response['content_type'] = r.headers['content-type']
        #    raise
    else:
        logger.error('transform_url(): Non text MIME Type; %s' % url)
        
        transformed_response['content'] = original_response['content']
        transformed_response['content_type'] = original_response['content_type']
        
    return transformed_response
    
    
def form_url(url, encode=False, site=None):
    if encode:
        if site:
            return reverse('fetch_coded', args={'site_domain': site.domain, 'url': encode_url(url)})
        else:
            return reverse('fetch_coded', args=[encode_url(url)])
    else:
        if site:
            return reverse('fetch', kwargs={'site_domain': site.domain, 'url': url})
        else:
            return reverse('fetch', args=[url])    


@print_timing       
def intercept_links(soup, url, encode=False, site=None):
    #if encode:
        # Encode images path
        for image in soup.findAll('img'):
            if image.get('src'):
                image['src'] = form_url(image['src'], url)

    # Prepend mechanic's url to all links
    for link in soup.findAll('a'):
        if link.get('href'):
            if is_external_top_level_link(link['href']) and not link.get('href').startswith('#'):
                pass
            else:
                link['href'] = form_url(link['href'], encode, site)

    # Prepend mechanic's url to all links
    for link in soup.findAll('link'):
        if link.get('href'):
            link['href'] = form_url(link['href'], encode, site)
            
    # Prepend mechanic's url to all links
    for script in soup.findAll('script'):
        if script.get('src'):
            script['src'] = form_url(script['src'], encode, site)    
    
    return soup        
