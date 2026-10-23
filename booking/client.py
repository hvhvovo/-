import requests
import time

class ApiError(AssertionError):
    pass

class Client:
    def __init__(self, base_url, session=None, trace=None):
        self.base_url = base_url.rstrip('/')
        self.trace = trace if trace is not None else []
        self.session = session or requests.Session()

    def call(self, method, path, expected, **kwargs):
        started = time.perf_counter()
        try:
            res = self.session.request(method, self.base_url + path,
                timeout=(10, 20), headers={'Accept': 'application/json'}, **kwargs)
        except requests.RequestException as exc:
            self.trace.append({'method': method, 'path': path, 'error': type(exc).__name__})
            raise ApiError(f'{method} {path}: network failure ({type(exc).__name__}); '
                           'not a confirmed product defect') from exc
        self.trace.append({'method': method, 'path': path, 'status': res.status_code,
                           'elapsed_ms': round((time.perf_counter() - started) * 1000, 3)})
        assert res.status_code == expected, (
            f'{method} {path}: expected {expected}, got {res.status_code}; {res.text[:500]}')
        return res

    def json(self, method, path, expected, **kwargs):
        res = self.call(method, path, expected, **kwargs)
        try:
            return res.json()
        except ValueError as exc:
            raise ApiError('Invalid JSON: ' + res.text[:300]) from exc
