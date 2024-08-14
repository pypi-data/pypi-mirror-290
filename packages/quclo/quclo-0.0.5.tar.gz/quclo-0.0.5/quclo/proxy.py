"""Proxy functions for QuClo."""

from functools import wraps
import requests
from quclo.utils import QUCLO_API_URL
from quclo.models import Priority, Backend
from quclo.config import Config


def proxy(
    func=None,
    *,
    url: str = QUCLO_API_URL,
    token: str | None = Config.load_token(),
    priority: Priority | None = None,
    backend: Backend | None = None,
):
    """Function and decorator to proxy requests globally or locally."""

    if priority is None and backend is None:
        priority = Priority.BALANCED

    def set_proxy():
        if getattr(requests.post, "_is_quclo_proxy", False):
            return requests.post
        else:
            original_post = requests.post

            def wrapped_post(*args, **kwargs):
                if token:
                    kwargs["headers"] = {"Authorization": f"Bearer {token}"}
                payload_key = "json" if "json" in kwargs else "data"
                if priority is not None:
                    kwargs[payload_key]["quclo_priority"] = priority.value
                elif backend is not None:
                    kwargs[payload_key]["quclo_backend"] = backend.name
                kwargs[payload_key]["quclo_url"] = args
                return original_post(url, **kwargs)

            requests.post = wrapped_post
            requests.post._is_quclo_proxy = True
            return original_post

    def decorator(inner_func):
        @wraps(inner_func)
        def wrapper(*args, **kwargs):
            original_post = set_proxy()
            try:
                return inner_func(*args, **kwargs)
            finally:
                requests.post = original_post

        return wrapper

    if func is None:
        set_proxy()
        return decorator
    elif callable(func):
        return decorator(func)
    else:
        raise ValueError("Invalid argument provided")
