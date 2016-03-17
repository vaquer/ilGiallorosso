import hmac
import re
import urllib
from django.conf import settings

THUMBRIO_API_KEY = settings.THUMBRIO_API_KEY
THUMBRIO_SECRET_KEY = settings.THUMBRIO_SECRET_KEY
THUMBRIO_BASE_URLS = settings.THUMBRIO_BASE_URLS


def _thumbrio_quote(s):
    return urllib.quote(s, safe='/-_.')


def thumbrio(url, size, thumb_name='thumb.png', query_arguments=None,
             base_url=THUMBRIO_BASE_URLS[0]):
    # we take out the http:// protocol as that's our default protocol
    unprefixed_url = re.sub(r'^http://', '', url).encode('utf-8')
    encoded_url = _thumbrio_quote(unprefixed_url)
    encoded_size = _thumbrio_quote(size)
    encoded_thumb_name = _thumbrio_quote(thumb_name)
    path = '%s/%s/%s' % (encoded_url, encoded_size, encoded_thumb_name)

    if query_arguments:
        if isinstance(query_arguments, str):
            qs = query_arguments.lstrip('?')
        else:
            qs = urllib.urlencode(query_arguments)
        path += '?' + qs

    # We should add the API to the URL when we use the non customized
    # thumbr.io domains
    if base_url in THUMBRIO_BASE_URLS:
        path = '%s/%s' % (THUMBRIO_API_KEY, path)

    # some bots (msnbot-media) "fix" the url changing // by /, so even if
    # it's legal it's troublesome to use // in a URL.
    path = path.replace('//', '%2F%2F')
    token = hmac.new(THUMBRIO_SECRET_KEY, base_url + path).hexdigest()
    return '%s%s/%s' % (base_url, token, path)