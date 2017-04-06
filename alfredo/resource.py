import ruamel.yaml as yaml

from alfredo.http import HttpService
from alfredo.mixins.lazy import LazyMixin
from alfredo.mixins.nested import NestedMixin


class HttpResource(NestedMixin, LazyMixin):
    def __init__(self, parent, path, children):
        LazyMixin.__init__(self)
        NestedMixin.__init__(self, parent, path, children)

        self.headers = []
        self.http_service = None

    @property
    def http(self):
        if not self.root.http_service:
            self.root.http_service = HttpService()
        return self.root.http_service

    def retrieve(self):
        return self.parse_response(self.http.get(self.full_path, self.root.headers))

    def create(self, **kwargs):
        return self.parse_response(self.http.post(self.full_path, self.root.headers, **kwargs))

    def replace(self, **kwargs):
        return self.parse_response(self.http.put(self.full_path, self.root.headers, **kwargs))

    def update(self, **kwargs):
        return self.parse_response(self.http.patch(self.full_path, self.root.headers, **kwargs))

    def delete(self):
        return self.parse_response(self.http.delete(self.full_path, self.root.headers))

    def parse_response(self, http_response):
        if http_response.ok and http_response.status_code != 204:
            response_body = http_response.json()
            if 'results' in response_body and 'count' in response_body:
                return HttpIterableResponse(self, http_response)

        return HttpSingleResponse(self, http_response)


class HttpPropertyResource(HttpResource):
    def __init__(self, parent, path, children):
        super(HttpPropertyResource, self).__init__(parent, path, children)

    def __getattr__(self, child_path):
        if child_path in self.value:
            return self.value[child_path]
        elif (":%s" % child_path) in self.children:
            return HttpMethodResource(self, child_path, self.children[(":%s" % child_path)])
        elif child_path in self.children:
            return HttpPropertyResource(self, child_path, self.children[child_path])
        else:
            try:
                return self.value.__getattr__(child_path)
            except AttributeError:
                raise AttributeError('%r object has no attribute %r' % (self.value.__class__.__name__, child_path))


class HttpMethodResource(HttpPropertyResource):
    def __init__(self, parent, path, children):
        super(HttpMethodResource, self).__init__(parent, path, children)

    def __call__(self, path):
        self.path = str(path)
        return self


class HttpResponse(HttpPropertyResource):
    def __init__(self, resource, status, reason, result):
        super(HttpResponse, self).__init__(resource.parent, resource.path, resource.children)
        self._status = status
        self._reason = reason
        self._result = result
        self._ok = True

    @property
    def status(self):
        return self._status

    @property
    def ok(self):
        return self._ok and self._status < 400

    def retrieve(self):
        return self._result

    def __str__(self):
        return yaml.dump(self.value, default_flow_style=False).rstrip('\n')

    def __repr__(self):
        return "\n%d - %s\n\n%s\n" % (self._status, self._reason, self)

    def __getitem__(self, item):
        key = list(self.value.keys())[item]
        return key, self.value[key]


class HttpSingleResponse(HttpResponse):
    def __init__(self, resource, http_response):
        super(HttpSingleResponse, self).__init__(resource, http_response.status_code, http_response.reason, {})

        if self._status != 204:
            try:
                self._result = http_response.json()
            except ValueError:
                self._result = {'detail': 'Unknown error'}
                self._ok = False


class HttpIterableResponse(HttpResponse):
    def __init__(self, resource, http_response):
        super(HttpIterableResponse, self).__init__(resource, http_response.status_code, http_response.reason,
                                                   http_response.json())

    def __len__(self):
        return self.value['count']

    def __str__(self):
        return "items: %d" % (len(self),)

    @property
    def items(self):
        return self.value['results']

    def __getitem__(self, key):
        if isinstance(key, slice):
            return iter(self[i] for i in range(*key.indices(len(self))))
        elif isinstance(key, int):
            if key < 0:
                key += len(self)
            if key < 0 or key >= len(self):
                raise IndexError("The index (%d) is out of range." % key)
            while key >= len(self.items):
                current_next = self.value['next']
                self.get_next_page()
                if current_next == self.value['next']:
                    raise IndexError("The index (%d) is out of range." % key)

            if ':id' in self.children and 'id' in self.items[key]:
                return HttpResponse(HttpPropertyResource(self, self.items[key]['id'], self.children[':id']),
                                    200, 'Partial content', self.items[key])
            else:
                return HttpResponse(self, 206, 'Partial content', self.items[key])
        else:
            raise TypeError('invalid argument')

    def get_next_page(self):
        if self.value['next']:
            next_page_value = self.http.get(self.value['next'], self.root.headers).json()
            self.value['results'].extend(next_page_value['results'])
            self.value['next'] = next_page_value['next']
