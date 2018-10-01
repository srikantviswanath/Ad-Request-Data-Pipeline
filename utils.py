import time


def timeit(desc='', persist_to_log=''):
    """
    Simple decorator to compute time of wrapped function
    :param str optional desc: Description of the wrapped function. If not provided uses the wrapped function name
    :param str optional persist_to_log: if provided, write the time computed to the text file
    :return:
    """
    def time_decorator(func):

        def wrapper(*args, **kwargs):
            start = time.time()
            response = func(*args, **kwargs)
            time_taken_ms = (time.time() - start) * 1000
            print('Time taken for %s: %s ms' % (desc if desc else func.__name__, time_taken_ms))
            if persist_to_log:
                with open(persist_to_log, 'a+') as f:
                    f.write(str(time_taken_ms) + ' ')
            return response

        return wrapper

    return time_decorator


