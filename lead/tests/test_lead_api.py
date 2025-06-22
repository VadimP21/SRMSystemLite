import json
import unittest
import tornado.testing
from tornado.httpclient import HTTPRequest, HTTPClientError

from lead.app import app


class TestApp(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return app()

    async def async_fetch(self, url, method="GET", body=None, headers=None):
        req = HTTPRequest(url=self.get_url(url), method=method, body=body, headers=headers)
        try:
            response = await self.http_client.fetch(req)
            return response
        except HTTPClientError as e:
            return e.response

    async def test_get_leads(self):
        response = await self.async_fetch('/leads')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body)
        self.assertIn('leads', data)


if __name__ == "__main__":
    unittest.main()