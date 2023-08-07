import requests
from django.conf import settings


def send_request_to_api_kit_service(uri: str=None, method='GET', data: dict = None, *args, **kwargs):
    session = requests.Session()
    header = {
        'Authorization': 'Bearer ggfgfghgggf'
    }
    kwargs['headers'] = {**kwargs['headers'], **header} if kwargs.get('headers') else header
    session.headers.update(kwargs['headers'])
    if method == 'POST' and data:
        kwargs['json'] = data
        kwargs['data'] = data
    return session.request(method=method, url=f'{settings.API_KIT_SERVICE}/{uri}', **kwargs)
