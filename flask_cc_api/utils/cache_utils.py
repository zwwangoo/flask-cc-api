import urllib

from flask import request

from ..extensions import cache


def cache_clear(*key):
    def decorator(func):
        def wrapper(*args, **kw):
            cache.clear()
            return func(*args, **kw)
        return wrapper
    return decorator


def cache_key():
    args = request.args
    key = request.path + '?' + urllib.parse.urlencode([
        (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    ])
    return key
