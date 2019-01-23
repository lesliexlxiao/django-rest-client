import json

from functools import wraps


def json_format(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        kwargs.setdefault('headers', {})
        if not kwargs['headers'].get('Content-Type'):
            kwargs['headers']['Content-Type'] = 'application/json'
        if not kwargs['headers'].get('Accept'):
            kwargs['headers']['Accept'] = 'application/json'

        if kwargs.get('data') is not None:
            try:
                kwargs['data'] = json.dumps(kwargs['data'])
            except:
                pass

        return func(*args, **kwargs)
    return func_wrapper
