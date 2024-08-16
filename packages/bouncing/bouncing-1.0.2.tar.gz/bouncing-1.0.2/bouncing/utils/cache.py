#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File    ：cache.py
# @Author  ：Jay
# @Date    ：2024/8/16 14:22 
# @Remark  ：
import xxhash
import pickle
import functools
import cachetools


def ttl_cache(ttl=20, maxsize=1000):
    def decorator(func):
        cache = cachetools.TTLCache(maxsize=maxsize, ttl=ttl)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = pickle.dumps((args, kwargs), protocol=pickle.HIGHEST_PROTOCOL)
            key_hash = xxhash.xxh64(key).hexdigest()
            if key_hash in cache and kwargs.pop("enable_cache", True):
                return cache[key_hash]

            result = func(*args, **kwargs)
            cache[key_hash] = result
            return result

        return wrapper

    return decorator


__all_ = ["ttl_cache"]
