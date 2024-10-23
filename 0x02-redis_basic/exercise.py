#!/usr/bin/env python3
"""Defines a class for interacting with Redis"""

from functools import wraps
import redis
from typing import Any, Callable, Union, Optional
import uuid


def replay(method: Callable) -> None:
    """Displays the history of calls to `method`.
    Shows the number of calls, and inputs/outputs of each call
    """
    r = redis.Redis(decode_responses=True)
    key = method.__qualname__
    count = r.get(key)
    print(f"{key} was called {count} times:")

    def hist(io):
        return r.lrange(f"{key}:{io}", 0, -1)

    for arg, res in zip(hist("inputs"), hist("outputs")):
        print(f"{key}(*{arg}) -> {res}")


def count_calls(method: Callable) -> Callable:
    """Decorator for counting and caching the number of calls to `method`"""

    @wraps(method)
    def wrapper(*args, **kwargs):
        key = method.__qualname__
        ret = method(*args, **kwargs)
        self = args[0]
        self._redis.incr(key)
        return ret

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator for storing the arguments and results for `method`"""

    @wraps(method)
    def wrapper(*args, **kwargs):
        self = args[0]
        key_in = f"{method.__qualname__}:inputs"
        key_out = f"{method.__qualname__}:outputs"
        self._redis.rpush(key_in, str(args[1:]))
        ret = method(*args, **kwargs)
        self._redis.rpush(key_out, ret)
        return ret

    return wrapper


class Cache:
    """Contains methods for interacting with a redis database"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data in redis using a random key.

        Args:
            data -  the variable to store

        Returns:
            str - the key associated with data in redis
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """Returns the value stored with `key`.
        The variable is decoded using the function `fn`
        """
        data = self._redis.get(key)

        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        """Returns a string stored with `key`"""
        return self.get(key, fn=lambda s: s.decode())

    def get_int(self, key: str) -> int:
        """Returns an integerr stored with `key`"""
        return self.get(key, fn=lambda s: int(s.decode()))
