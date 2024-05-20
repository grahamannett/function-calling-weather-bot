from typing import Sequence
import time
from functools import wraps


def retry(
    max_retries: int = 3,
    delay: int = 1,
    backoff: int = 2,
    exceptions: Sequence[Exception] = (Exception,),
) -> callable:
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
