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


def use_mock_http(f, *args, **kwargs):
    return responses.activate(f, *args, **kwargs)


def mock_http_uri(method, url, callback=None, json=None, status=None, text=None):
    if callback:
        return responses.add_callback(method, url, callback=callback, content_type='application/json')
    if text:
        return responses.add(method, url, body=text)
    if json:
        return responses.add(method, url, json=json)
    if status:
        return responses.add(method, url, status=status)


def mock_http():
    mock_http_uri(GET, 'https://beta.rstor.io/users/me/', json={'first_name': 'Bob'})
    mock_http_uri(PUT, 'https://beta.rstor.io/users/me/', callback=echo)
    mock_http_uri(PATCH, 'https://beta.rstor.io/users/me/', callback=echo)
    mock_http_uri(POST, 'https://beta.rstor.io/apps/', callback=echo)
    mock_http_uri(GET, 'https://beta.rstor.io/apps/', json={'count': 1, 'results': [{'id': 1, 'name': 'Octave'}]})
    mock_http_uri(GET, 'https://beta.rstor.io/apps/1/', json={'name': 'Octave'})
    mock_http_uri(DELETE, 'https://beta.rstor.io/apps/1/', status=204)
    mock_http_uri(GET, 'https://beta.rstor.io/files/', json={'count': 0, 'results': []})
    mock_http_uri(GET, 'https://beta.rstor.io/jobs/1/stdout/', text='hello\n')
    mock_http_uri(GET, 'https://beta.rstor.io/users/', status=404)
    mock_http_uri(GET, 'https://beta.rstor.io/jobs/', status=500)
    # mock_http_uri(POST, 'https://beta.rstor.io/files/', callback=echo)


def echo(request):
    payload = dict(parse_qsl(request.body))
    return 200, {}, json.dumps(payload)


def echo_file(request):
    payload = dict(parse_qsl(request.body))
    print(payload)
    return 200, {}, json.dumps({'name': payload['file'].name})
