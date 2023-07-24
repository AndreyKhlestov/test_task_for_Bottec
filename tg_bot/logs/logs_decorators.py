import functools


def catch_exception(logger, placeholder: str = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"{placeholder}\n{e}")
                raise

        return wrapper

    return decorator


def silent_exception():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                pass

        return wrapper

    return decorator
