from franklin_fastapi_extension import GET, POST, PUT
from .mock_dto import MockDTO


@GET("/get")
def get_mock_router():
    return {"message": "GET method"}


@POST("/post")
def post_mock_router(mock_dto: MockDTO):
    return {"message": mock_dto.message}


@PUT("/put")
def put_mock_router(mock_dto: MockDTO):
    return {"message": mock_dto.message}

