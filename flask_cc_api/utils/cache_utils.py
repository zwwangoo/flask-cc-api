import urllib

from functools import wraps
from flask import request

from ..extensions import cache


def cache_clear(fn):
    @wraps
    def wrapper(*args, **kwargs):
        cache.cache_clear()
        return fn(*args, **kwargs)
    return wrapper


def cache_key():
    args = request.args
    key = request.path + '?' + urllib.parse.urlencode([
        (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    ])
    return key
