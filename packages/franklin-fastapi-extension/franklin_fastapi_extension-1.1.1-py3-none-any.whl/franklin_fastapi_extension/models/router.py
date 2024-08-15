from fastapi import FastAPI, APIRouter
from functools import wraps
import importlib
import pkgutil
import inspect

_all_routers = []


def register_routes(app: FastAPI, route_module: object):
    """
    Register all the routers with the FastAPI app.
    :param app: The FastAPI app
    :param route_module: The module containing the route definitions
    :return: None
    """

    # Get all the modules in the package
    modules = pkgutil.iter_modules(route_module.__path__)

    for module_info in modules:
        # Import the module
        module = importlib.import_module(f"{route_module.__name__}.{module_info.name}")

        # Create an APIRouter for this module
        router = APIRouter()

        # Base path derived from the module name
        base_path = module_info.name.replace('_', '-')

        # Get all the functions in the module
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and hasattr(obj, 'route_info'):
                # Retrieve route path and method
                route_path, method = obj.route_info
                full_path = f"/{base_path}{route_path}"

                # Add the route to the router
                router.add_api_route(full_path, obj, methods=[method])

        # Include the router in the FastAPI app
        app.include_router(router)


def route(path: str, method: str):
    """
    A generic route decorator that stores the route info on the method.
    :param path: The route path
    :param method: The HTTP method
    :return: The wrapped function with route info
    """

    def decorator(func: callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        wrapper.route_info = (path, method)
        return wrapper

    return decorator


def GET(path: str = None):
    return route(path, "GET")


def PUT(path: str = None):
    return route(path, "PUT")


def POST(path: str = None):
    return route(path, "POST")


def DELETE(path: str = None):
    return route(path, "DELETE")


def PATCH(path: str = None):
    return route(path, "PATCH")
