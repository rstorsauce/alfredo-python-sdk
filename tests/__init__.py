import json

try:
    from urlparse import parse_qsl
except ImportError:
    from urllib.parse import parse_qsl

import responses

GET = responses.GET
PUT = responses.PUT
DELETE = responses.DELETE
PATCH = responses.PATCH
POST = responses.POST


def echo(request):
    payload = dict(parse_qsl(request.body))
    return 200, {}, json.dumps(payload)


def basic_response(status, body):
    def response(*args, **kwargs):
        return status, {}, body

    return response


def mock_http_uri(method, path, callback=None, result=None, status=200, text=None):
    url = "{base!s}{path!s}".format(base='https://apibeta.rstor.io', path=path)

    content_type = 'application/json'
    if result:
        callback = basic_response(status, json.dumps(result))
    if text:
        content_type = 'text/plain'
        callback = basic_response(status, text)
    if not callback:
        callback = basic_response(status, '{}')

    return responses.add_callback(method, url, callback=callback, content_type=content_type)


def use_mock_http(f, *args, **kwargs):
    return responses.activate(f, *args, **kwargs)


def mock_http():
    mock_http_uri(POST, '/sso/token-by-email/', result={'token': 'faketoken'})
    mock_http_uri(GET, '/users/me/', result={'first_name': 'Bob'})
    mock_http_uri(PUT, '/users/me/', callback=echo)
    mock_http_uri(PATCH, '/users/me/', callback=echo)
    mock_http_uri(POST, '/apps/', callback=echo)
    mock_http_uri(GET, '/apps/', result={'count': 1, 'results': [{'id': 1, 'name': 'Octave'}]})
    mock_http_uri(GET, '/apps/1/', result={'name': 'Octave'})
    mock_http_uri(DELETE, '/apps/1/', status=204)
    mock_http_uri(GET, '/files/', result={'count': 0, 'results': []})
    mock_http_uri(GET, '/jobs/1/stdout/', text='hello')
    mock_http_uri(GET, '/users/', status=404)
    mock_http_uri(GET, '/jobs/', status=500)
