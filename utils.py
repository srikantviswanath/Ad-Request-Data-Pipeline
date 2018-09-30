import time

import expiringdict


def timeit(desc=''):
    """Simple decorator to compute time of wrapped function"""
    def time_decorator(func):

        def wrapper(*args, **kwargs):
            start = time.time()
            response = func(*args, **kwargs)
            time_taken_ms = (time.time() - start) * 1000
            print('Time taken for %s: %s ms' % (desc if desc else func.__name__, time_taken_ms))
            return response

        return wrapper

    return time_decorator


def timed_memoize(ttl, cache_size=10**7):
    """
    Timed cache. After expiry of :ttl: wrapped function's input args will be evicted
    :param int ttl: Time to live in seconds
    :param int cache_size: number of keys the cache can hold
    :return:
    """
    cache = expiringdict.ExpiringDict(cache_size, ttl)

    def wrapper(func):
        def memoized_func(*args):
            if args in cache:
                return cache[args]
            result = func(*args)
            cache[args] = result
            return result
        return memoized_func

    return wrapper

