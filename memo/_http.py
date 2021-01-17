from functools import wraps

import httpx


def memweb(url: str):
    """
    Remembers input/output of a function by sending it over http to an endpoint.

    Important:
        Note that this decorator requires an extra dependeny. Ensure it is installed
        properly by running either;

        ```
        python -m pip install "memo[web]"
        ```

        You can also install it by installing all optional dependencies.

        ```
        python -m pip install "memo[all]"
        ```

    Arguments:
        url: web url to post json to
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with httpx.Client() as client:
                _ = client.post(url, data={**kwargs, **result})
            return result

        return wrapper

    return decorator
