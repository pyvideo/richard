from collections import namedtuple


Browser = namedtuple('Browser', [
        'name', 'version', 'platform_version', 'mobile', 'tablet'])


def parse_ua(ua):
    # TODO: Flesh this out--it's ultra-basic and barely meets my
    # needs.
    data = {
        'name': '',
        'version': None,
        'platform_version': '',
        'mobile': False,
        'tablet': False
        }

    ua = ua.lower()
    if 'firefox' in ua:
        data['name'] = 'Firefox'

    if 'mobile' in ua:
        data['mobile'] = True
    elif 'tablet' in ua:
        data['tablet'] = True

    return Browser(**data)


class BrowserDetectMiddleware(object):
    """
    Detects browser bits from the UA and flags the request
    accordingly.
    """
    def process_request(self, request):
        ua = request.META.get('HTTP_USER_AGENT', '')
        request.BROWSER = parse_ua(ua)
