from fastapi import Request
from fastapi.responses import JSONResponse
from factories import *
from .response import Response
from .dto import DTO


def _handle_errors(result: Response) -> JSONResponse:
    if result is None:
        return not_found_response()
    elif result.errors:
        return create_response(result, 'internal_server_error')
    else:
        return success_response(result)


async def get_all(supplier: callable) -> JSONResponse:
    """
    A Helper function to handle the get all for the service handling any errors
    :param supplier: The service function to call which returns a Response object
    :return:
    """
    result = supplier()

    return _handle_errors(result)


async def get_by_params(function: callable, params: any) -> JSONResponse:
    if params:
        result = function(params)
        return _handle_errors(result)
    else:
        return bad_request_response()


async def call_request(function: callable, body: Request, dtoClass: DTO) -> JSONResponse:
    """
    A helper function to handle requests with request body validation. Must be used with the await keyword.
    :param function: A callable function that takes in the classType as a parameter
    :param body: The request body, which will be validated against the classType
    :param dtoClass: The DTO class to validate the request body against
    :return: JSONResponse
    """

    data = await body.json()
    data = dtoClass(**data)

    errors = dtoClass.validate(data)
    if not errors:
        result = function(data)
        return _handle_errors(result)
    else:
        return bad_request_response(Response(errors=errors))
