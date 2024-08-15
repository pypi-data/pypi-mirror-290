from franklin_fastapi_extension import GET, POST, PUT, call_request, Request, get_all
from .mock_dto import MockDTO
from .mock_service import get_all as get, post_request


@GET("/get")
async def get_mock_router():
    return await get_all(get)


@POST("/post")
async def post_mock_router(mock_dto: Request):
    return await call_request(post_request, mock_dto, MockDTO)


@PUT("/put")
async def put_mock_router(mock_dto: Request):
    return await call_request(post_request, mock_dto, MockDTO)

