from functools import wraps


def func_decor(func):

    @wraps(func)
    def inner(*args, **kwargs):
        print(f"{func.__name__} be decorated.")
        return func(*args, **kwargs)

    return inner