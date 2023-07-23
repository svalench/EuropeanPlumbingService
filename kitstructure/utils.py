import requests
from django.conf import settings


def send_request_to_api_kit_service(uri: str=None, method='GET', data: dict = None):
    session = requests.Session()
    kwargs= {}
    header = {
        'Authorization': 'Bearer ggfgfghgggf'
    }
    session.headers.update(header)
    if method == 'POST' and data:
        kwargs['json'] = data
    return session.request(method=method, url=f'{settings.API_KIT_SERVICE}/{uri}', **kwargs)
