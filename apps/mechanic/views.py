import logging
from urllib2 import HTTPError

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from mechanic.api import transform_url

logger = logging.getLogger(__name__)


def fetch(request, url=None):
    url = request.GET.get('url', url)
    logger.debug('fetch(): url: %s' % url)
    try:
        transformed_response = transform_url(url)
    except HTTPError:
        #if status_code == requests.codes.NOT_FOUND:
        return render_to_response('http_error_not_found.html', {},
            context_instance=RequestContext(request))
    else:
        return HttpResponse(
            content=transformed_response.get('content', ''),
            status=transformed_response.get('status_code', 200),
            content_type=transformed_response.get('content_type')
        )
