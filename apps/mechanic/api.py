import re
import urlparse
import logging
    
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode, force_unicode, smart_str, DjangoUnicodeDecodeError
from django.db.models import Q

import mechanize
from bs4 import BeautifulSoup, UnicodeDammit
import requests
from HTMLParser import HTMLParseError

from mechanic.literals import ATTRIBUTE_CONTENT, COMPARISON_ICONTAINS, \
    COMPARISON_CONTAINS, COMPARISON_EQUALS, OPERAND_OR, OPERAND_AND, \
    ACTION_REMOVE, ACTION_REPLACE
from mechanic.models import TransformationRule
from mechanic.utils import unescape, encode_url

logger = logging.getLogger(__name__)

USE_MECHANIZE = False


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
       
        if element_comparison.attribute_comparison == COMPARISON_ICONTAINS or element_comparison.attribute_comparison == COMPARISON_CONTAINS:
            if element_comparison.attribute_comparison == COMPARISON_ICONTAINS:
                flag = re.I
            else:
                flag = 0
            if element_comparison.negate:
                if rule_dictionary.get('text', False):
                    if not re.search(element_comparison.value, element, flag):
                        results.append(element)
                else:
                    attribute_value = element.get(attribute)
                    if attribute_value:
                        if not re.search(element_comparison.value, attribute_value, flag):
                            results.append(element)
            else:
                if rule_dictionary.get('text', False):
                    if re.search(element_comparison.value, element, flag):
                        results.append(element)
                else:
                    attribute_value = element.get(attribute)
                    if attribute_value:
                        if re.search(element_comparison.value, attribute_value, flag):
                            results.append(element)

        elif element_comparison.attribute_comparison == COMPARISON_EQUALS:
            if element_comparison.negate:
                if rule_dictionary.get('text', False):
                    if element_comparison.value != element:
                        results.append(element)
                else:
                    attribute_value = element.get(attribute)
                    if attribute_value:
                        if element_comparison.value != attribute_value:
                            results.append(element)
            else:
                if rule_dictionary.get('text', False):
                    if element_comparison.value == element:
                        results.append(element)
                else:
                    attribute_value = element.get(attribute)
                    if attribute_value:
                        if element_comparison.value == attribute_value:
                            results.append(element)

    return set(results)


def transform_url(url, site):
    transformed_response = {}
    
    if USE_MECHANIZE:
        br = mechanize.Browser(factory=mechanize.RobustFactory())
        response = br.open(url)
        status_code = response._headers.status
        html = response.read()
        content_type = response._headers.typeheader
    else:
        transformed_response = {}
        response = requests.get(url, allow_redirects=True)
        transformed_response['status_code'] = response.status_code
        html = response.content
        content_type = response.headers['content-type']
        
    if 'text' in content_type:
        try:
            if not USE_MECHANIZE:
                response.raise_for_status()
            
            #html = unescape(html)
            #html = unicode(BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES))
            try:
                html = smart_unicode(html)
            except DjangoUnicodeDecodeError:
                pass
            soup = BeautifulSoup(html)
            #, smartQuotesTo=None)
            #, fromEncoding="windows-1252")
            # Convert all images' relative path to an absolute path
            for image in soup.findAll('img'):
                if image.get('src'):
                    image['src'] = fix_relative_url(image['src'], url)

            # Convert links url to absolute and prepend mechanic's url to all links
            for link in soup.findAll('a'):
                if link.get('href'):
                    if is_external_top_level_link(link['href']) and not link.get('href').startswith('#'):
                        pass
                        #link.extract()
                    else:
                        href = fix_relative_url(link['href'], url)
                        link['href'] = form_url(href, site)

            # Convert css links url to absolute and prepend mechanic's url to all links
            for link in soup.findAll('link'):
                if link.get('href'):
                    href = fix_relative_url(link['href'], url)
                    link['href'] = form_url(href, site)
                    
            # Convert scripts links url to absolute and prepend mechanic's url to all links
            for script in soup.findAll('script'):
                if script.get('src'):
                    href = fix_relative_url(script['src'], url)
                    script['src'] = form_url(href, site)

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

                elements = soup.findAll(**rule_dictionary)
                element_comparison_result = None
                for element_comparison in rule.elementcomparison_set.all():
                    results = compare_elements(elements, element_comparison, rule_dictionary, source_attribute)
                    if element_comparison_result is None:
                        element_comparison_result = results
                    else:
                        if element_comparison.attribute_comparison_operand == OPERAND_AND:
                            element_comparison_result &= results
                        else:
                            element_comparison_result |= results

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
                            if rule.attribute == ATTRIBUTE_CONTENT:
                                eval_result = eval(rule.action_argument, {
                                        'source': result_element,
                                        'fetch_url': reverse('fetch'),
                                        'fetch_coded_url': reverse('fetch_coded')
                                    }
                                )
                                result_element.replaceWith(eval_result)
                            else:
                                    eval_result = eval(rule.action_argument, {
                                            'source': result_element[rule.attribute],
                                            'fetch_url': reverse('fetch'),
                                            'fetch_coded_url': reverse('fetch_coded')
                                        }
                                    )
                                    result_element[rule.attribute] = eval_result
                        except Exception, err:
                            raise Exception('Error handling rule: "%s"; error: %s' % (rule, err))

            #soup = encode_urls(soup)
            transformed_response['content'] = soup.prettify()

        #except (HTMLParseError, UnicodeDecodeError, RuntimeError), err:
        except (HTMLParseError, RuntimeError), err:
            logger.error('transform_url(): HTMLParseError, or RuntimeError')
            
            transformed_response['content'] = html
            transformed_response['content_type'] = content_type


        #except AttributeError:
        #    transformed_response['content'] = 'No content'
        #    transformed_response['content_type'] = ''

        #except HTTPError:
            #transformed_response['status_core'] = r.status_code
        #    raise

        #except Exception, err:
        #    logger.debug('transform_url(): Unhandled exception: %s' % err)
        #    transformed_response['content'] = response.read()
        #    transformed_response['content_type'] = r.headers['content-type']
        #    raise
    else:
        transformed_response['content'] = html
        transformed_response['content_type'] = content_type
        
    return transformed_response
    
    
def form_url(url, site=None):
    if site:
        return reverse('fetch', kwargs={'site_domain': site.domain, 'url': url})
    else:
        return reverse('fetch', args=[url])    


def encode_urls(soup, site=None):
    for image in soup.findAll('img'):
        if image.get('src'):
            image['src'] = form_final_url(image['src'], site)

    # Convert links url to absolute and prepend mechanic's url to all links
    for link in soup.findAll('a'):
        if link.get('href'):
            link['href'] = form_final_url(link['href'], site)

    # Convert css links url to absolute and prepend mechanic's url to all links
    for link in soup.findAll('link'):
        if link.get('href'):
            link['href'] = form_final_url(link['href'], site)
            
    # Convert scripts links url to absolute and prepend mechanic's url to all links
    for script in soup.findAll('script'):
        if script.get('src'):
            script['src'] = form_final_url(script['src'], site)
    
    return soup
    
    
def form_final_url(url, site=None):
    if site:
        return reverse('fetch_coded', args={'site_domain': site.domain, 'url': encode_url(url)})
    else:
        return reverse('fetch_coded', args=[encode_url(url)])
