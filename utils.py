import time

import expiringdict


def timeit(desc=''):

    def time_decorator(func):

        def wrapper(*args, **kwargs):
            start = time.time()
            response = func(*args, **kwargs)
            time_taken_ms = (time.time() - start) * 1000
            print('Time taken for %s: %s ms' % (desc if desc else func.__name__, time_taken_ms))
            return response

        return wrapper

    return time_decorator


def memoize(func):
    cache = expiringdict.ExpiringDict(10 ** 7, 86400)

    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return memoized_func

