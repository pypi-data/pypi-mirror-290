from fastapi.responses import JSONResponse
from ..models.response import Response


_status_codes = {
    'success': 200,
    'created': 201,
    'bad_request': 400,
    'unauthorized': 401,
    'forbidden': 403,
    'not_found': 404,
    'internal_server_error': 500,
}


def _generate_response(data: Response, status: str = 'success') -> JSONResponse:
    if status not in _status_codes:
        status = 'internal_server_error'
    if data is None:
        data = Response()

    return JSONResponse(
        content=data.dict(),
        status_code=_status_codes[status]
    )


def success_response(data: Response = None) -> JSONResponse:
    return _generate_response(data, 'success')


def created_response(data: Response = None) -> JSONResponse:
    return _generate_response(data, 'created')


def bad_request_response(data: Response = None) -> JSONResponse:
    return _generate_response(data, 'bad_request')


def unauthorized_response(data: Response = None) -> JSONResponse:
    return _generate_response(data, 'unauthorized')


def forbidden_response(data: Response = None) -> JSONResponse:
    return _generate_response(data, 'forbidden')


def not_found_response(data: Response = None) -> JSONResponse:
    return _generate_response(data, 'not_found')


def internal_server_error_response(data: Response = None) -> JSONResponse:
    return _generate_response(data, 'internal_server_error')


def create_response(data: Response = None, status='success') -> JSONResponse:
    return _generate_response(data, status)
