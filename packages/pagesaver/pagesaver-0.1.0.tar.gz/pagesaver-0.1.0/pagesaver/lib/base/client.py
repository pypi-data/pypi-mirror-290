from urllib.parse import urljoin

import requests


class BaseClient:
    def __init__(self, base_url) -> None:
        self.base_url = base_url
        self._client = None

    @property
    def client(self):
        return self._client

    def build_url(self, path, *args, **kwargs):
        raise NotImplementedError

    def build_headers(self, *args, **kwargs):
        raise NotImplementedError

    def do_request(self, method, url, headers=None, query=None, body=None, **kwargs):
        raise NotImplementedError

    def parse_response(self, response):
        raise NotImplementedError

    def make_request(self, method, path, query=None, body=None, **kwargs):
        url = self.build_url(path, query=query, body=body, **kwargs)
        headers = self.build_headers()
        return self.do_request(
            method, url, headers=headers, query=query, body=body, **kwargs
        )

    def request(self, method, path, query=None, body=None, **kwargs):
        response = self.make_request(method, path, query=query, body=body, **kwargs)
        return self.parse_response(response)

    def get(self, path, query=None, **kwargs):
        return self.request("GET", path, query=query, **kwargs)

    def post(self, path, body, **kwargs):
        return self.request("POST", path, body=body, **kwargs)

    def patch(self, path, body, **kwargs):
        return self.request("PATCH", path, body=body, **kwargs)

    def put(self, path, body, **kwargs):
        return self.request("PUT", path, body=body, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)


class RequestsBaseClient(BaseClient):
    DEFAULT_TIMEOUT = 5

    def __init__(self, base_url, timeout=DEFAULT_TIMEOUT) -> None:
        super().__init__(base_url=base_url)
        self._client = requests.Session()
        self.timeout = timeout

    def build_url(self, path, **kwargs):
        return urljoin(self.base_url, path)

    def do_request(self, method, url, headers=None, query=None, body=None, **kwargs):
        return requests.request(
            method,
            url,
            timeout=kwargs.pop("timeout", self.timeout),
            headers=headers,
            params=query,
            json=body,
            **kwargs,
        )

    def parse_response(self, response: requests.Response):
        response.raise_for_status
        if response.status_code != requests.codes.ok:
            raise requests.HTTPError(
                f"{response.status_code} {response.reason} for {response.url} {response.text}"
            )
        return response.json()
