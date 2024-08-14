from functools import wraps

from fastapi import FastAPI
from fastapi.routing import APIRouter
from inspect import signature


"""
Router Module

This module contains all the necessary decorators and functions needed to set up the API routes.
"""


_all_routers = []


def register_routes(app: FastAPI):
    """
    Register all the routers with the FastAPI app
    :param app: The FastAPI app
    :return: None
    """
    for router in _all_routers:
        app.include_router(router)


def Router(cls):
    router = APIRouter()

    for name, method in cls.__dict__.items():
        if hasattr(method, 'route_info'):
            path, http_method = method.route_info
            router.add_api_route(path, method, methods=[http_method])

    _all_routers.append(router)
    return cls


def route(path: str, method: str):
    """
    A generic route that stores the route info on the method
    :param path:
    :param method:
    :return:
    """
    def decorator(func: callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        wrapper.route_info = (path, method)
        return wrapper

    return decorator


def GET(path: str):
    return route(path, "GET")


def PUT(path: str):
    return route(path, "PUT")


def POST(path: str):
    return route(path, "POST")


def DELETE(path: str):
    return route(path, "DELETE")


def PATCH(path: str):
    return route(path, "PATCH")
