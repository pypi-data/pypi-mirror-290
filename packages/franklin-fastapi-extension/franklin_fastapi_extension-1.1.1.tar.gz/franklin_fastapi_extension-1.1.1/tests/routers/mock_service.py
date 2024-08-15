from franklin_fastapi_extension import Response
from .mock_dto import MockDTO


def post_request(dto: MockDTO) -> Response:
    return Response(node=dto, errors=None)

def get_all() -> Response:
    return Response(node={"message": "GET method"}, errors=None)

