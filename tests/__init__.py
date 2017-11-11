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


def mock_http_uri(method, url, callback=None, result=None, status=200, text=None):
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
    mock_http_uri(POST, 'https://beta.rstor.io/sso/token-by-email/', result={'token': 'faketoken'})
    mock_http_uri(GET, 'https://beta.rstor.io/users/me/', result={'first_name': 'Bob'})
    mock_http_uri(PUT, 'https://beta.rstor.io/users/me/', callback=echo)
    mock_http_uri(PATCH, 'https://beta.rstor.io/users/me/', callback=echo)
    mock_http_uri(POST, 'https://beta.rstor.io/apps/', callback=echo)
    mock_http_uri(GET, 'https://beta.rstor.io/apps/', result={'count': 1, 'results': [{'id': 1, 'name': 'Octave'}]})
    mock_http_uri(GET, 'https://beta.rstor.io/apps/1/', result={'name': 'Octave'})
    mock_http_uri(DELETE, 'https://beta.rstor.io/apps/1/', status=204)
    mock_http_uri(GET, 'https://beta.rstor.io/files/', result={'count': 0, 'results': []})
    mock_http_uri(GET, 'https://beta.rstor.io/jobs/1/stdout/', text='hello')
    mock_http_uri(GET, 'https://beta.rstor.io/users/', status=404)
    mock_http_uri(GET, 'https://beta.rstor.io/jobs/', status=500)
