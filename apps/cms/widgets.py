from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


def media_thumbnail(media):
    try:
        return mark_safe(u'<a class="fancybox" href="%(url)s"><img src="%(thumbnail)s" alt="%(string)s" /></a>' % {
            'url': reverse('media_preview', args=[media.pk]),
            'thumbnail': reverse('media_thumbnail', args=[media.pk]),
            'static_url': settings.STATIC_URL,
            'string': _(u'thumbnail')
        })
    except:
        return u''
