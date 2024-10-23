#!/usr/bin/env python3
"""Contains functions for tracking requests for a page"""

import requests
import redis
from functools import wraps


def cacheable(func):
    """Caches the result of a request."""

    @wraps(func)
    def wrapper(*args):
        r = redis.Redis(decode_responses=True)
        url = args[0]
        r.incr(f"count:{url}")
        cached = r.get(url)
        if cached:
            return cached

        html = func(*args)
        r.set(url, html, ex=10)
        return html

    return wrapper


@cacheable
def get_page(url: str) -> str:
    """Gets and returns the HTML content of the page at `url`

    Args
        url(str)

    Returns
        the url's HTML content
    """

    resp = requests.get(url)
    return resp.text
