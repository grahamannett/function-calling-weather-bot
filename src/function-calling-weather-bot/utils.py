import time
from functools import wraps
from typing import Sequence


def retry(
    max_retries: int = 3,
    delay: int = 1,
    backoff: int = 2,
    exceptions: Sequence[Exception] = (Exception,),
) -> callable:
    """
    Decorator function that allows retrying the decorated function in case of exceptions.

    Args:
        max_retries (int): The maximum number of retries.
        delay (int): The initial delay (in seconds) between retries.
        backoff (int): The backoff factor for increasing the delay between retries.
        exceptions (Sequence[Exception]): The exceptions to catch and retry on.

    Returns:
        callable: The decorated function.

    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_count = 0
            while retry_count < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        raise e
                    sleep_time = delay * (backoff ** (retry_count - 1))
                    time.sleep(sleep_time)

        return wrapper

    return decorator
