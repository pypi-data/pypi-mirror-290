"""_summary_"""
from functools import wraps

routes = {}


def route(app_route: str):
    """Register application route."""

    def function_route(func):
        routes[app_route] = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        return wrapper

    if callable(app_route):
        return function_route(app_route)
    return function_route
