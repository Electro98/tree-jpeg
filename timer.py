from functools import wraps
from time import time


def timeit(func):
    """Count execution time for functions."""
    @wraps(func)
    def modificated_func(*args, **kwargs):
        now = time()
        result = func(*args, **kwargs)
        end = time()
        print(f"[RESULT]: Function '{func.__name__}' time is {end - now} sec.")
        return result
    return modificated_func
