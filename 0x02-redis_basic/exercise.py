#!/usr/bin/env python3
"""
Module for redis exercise
"""

import redis
from typing import Union, Optional, Callable
from functools import wraps


class Cache:
    """
    Cache class
    """

    def __init__(self):
        """Initialize Redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @wraps
    def count_calls(method: Callable) -> Callable:
        """Decorator function to count number of times a method is called"""

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            """Wrapper function to increment count and call original method"""
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)

        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, bytearray]) -> str:
        """Store data in Redis and return key"""
        key = self._redis.incr("key")
        self._redis.set(key, data)
        return key

    def get(self, key: Union[str, int]) -> Optional[Union[str, bytes]]:
        """Get data from Redis"""
        if isinstance(key, int):
            key = str(key)
        return self._redis.get(key)

    def get_str(self, key: Union[str, int]) -> str:
        """Get data from Redis as string"""
        data = self.get(key)
        if data is not None:
            return data.decode("utf-8")
        return ""

    def get_int(self, key: Union[str, int]) -> int:
        """Get data from Redis as integer"""
        data = self.get(key)
        if data is not None:
            return int(data)
        return 0

    def get_list(self, key: Union[str, int]) -> list:
        """Get data from Redis as list"""
        data = self.get(key)
        if data is not None:
            return data.decode("utf-8").split(",")
        return []

    def get_calls(self, method: Callable) -> int:
        """Get number of times a method has been called"""
        key = method.__qualname__
        return self.get_int(key)
