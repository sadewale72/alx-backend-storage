#!/usr/bin/env python3
"""
Web cache and tracker
"""
import requests
import redis
from typing import Optional


def get_page(url: str) -> Optional[str]:
    """
    Get the HTML content of a URL and cache the result with an
    expiration time of 10 seconds.Track how many times a
    particular URL was accessed in the key "count:{url}".
    """
    r = redis.Redis()
    count_key = f"count:{url}"
    html = r.get(url)
    if html is None:
        response = requests.get(url)
        if response.status_code == 200:
            html = response.content
            r.set(url, html, ex=10)
            r.incr(count_key)
        else:
            return None
    else:
        r.incr(count_key)
    return html.decode('utf-8')
