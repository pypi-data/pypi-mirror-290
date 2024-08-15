import unittest
import httpx
from franklin_fastapi_extension import FastAPI, register_routes
from . import routers


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    app = FastAPI()
    client = None

    @classmethod
    def setUpClass(cls):
        cls.client = httpx.AsyncClient(app=cls.app, base_url="http://test")
        register_routes(cls.app, routers)

    @classmethod
    async def asyncTearDownClass(cls):
        await cls.client.aclose()

    async def test_get_mock_router(self):
        response = await self.client.get("/mock-router/get")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "GET method"})

    async def test_post_mock_router(self):
        response = await self.client.post("/mock-router/post", json={"message": "POST method"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "POST method"})

    async def test_put_mock_router(self):
        response = await self.client.put("/mock-router/put", json={"message": "PUT method"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "PUT method"})

    async def test_invalid_post_item(self):
        response = await self.client.post("/mock-router/post", json={"message": 1})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {'detail': [{'type': 'string_type', 'loc': ['body', 'message'],
                                                       'msg': 'Input should be a valid string', 'input': 1}]})

    async def test_invalid_put_item(self):
        response = await self.client.put("/mock-router/put", json={"message": 1})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {'detail': [{'type': 'string_type', 'loc': ['body', 'message'],
                                                       'msg': 'Input should be a valid string', 'input': 1}]})


if __name__ == '__main__':
    unittest.main()
