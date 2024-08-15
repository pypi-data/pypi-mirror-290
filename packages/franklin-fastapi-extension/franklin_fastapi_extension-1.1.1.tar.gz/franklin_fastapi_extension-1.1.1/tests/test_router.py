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
        self.assertEqual(
            {
                "node": {"message": "GET method"},
                "errors": None
            },
            response.json())

    async def test_post_mock_router(self):
        response = await self.client.post("/mock-router/post", json={"message": "POST method"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual({"node": {"message": "POST method"}, "errors": None}, response.json())

    async def test_put_mock_router(self):
        response = await self.client.put("/mock-router/put", json={"message": "PUT method"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual({"node": {"message": "PUT method"}, "errors": None}, response.json())

    async def test_invalid_post_item(self):
        response = await self.client.post("/mock-router/post", json={"message": 1})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            {
                "node": None,
                "errors":["Invalid type for message: expected str, got int"]
            },
            response.json())

    async def test_invalid_put_item(self):
        response = await self.client.put("/mock-router/put", json={"message": 1})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            {
                "node": None,
                "errors":["Invalid type for message: expected str, got int"]
            },
            response.json())


if __name__ == '__main__':
    unittest.main()