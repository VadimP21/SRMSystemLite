import json
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

    async def test_post_lead(self):
        payload = {
            "name": "Test User",
            "first_name": "Test",
            "phone": "+15551234567",
            "email": "test@example.com",
            "adv_id": 1,
        }
        response = await self.async_fetch('/leads', method="POST", body=json.dumps(payload),
                                          headers={'Content-Type': 'application/json'})
        self.assertEqual(response.code, 201)

        data = json.loads(response.body)
        self.assertIn('name', data)
        self.assertEqual(data['name'], 'Test User')
        self.assertEqual(data["first_name"], "Test")
        self.assertEqual(data["phone"], "+15551234567")
        self.assertEqual(data["email"], "test@example.com")
        self.assertEqual(data["adv_id"], 1)

    async def test_get_lead(self):
        payload = {
            "name": "Test User",
            "first_name": "Test",
            "phone": "+15551234567",
            "email": "test@example.com",
            "adv_id": 1,
        }
        response = await self.async_fetch('/leads', method="POST", body=json.dumps(payload),
                                          headers={'Content-Type': 'application/json'})
        self.assertEqual(response.code, 201)

        lead = json.loads(response.body)
        response = await self.async_fetch(f'/leads/{lead['id']}')
        self.assertEqual(response.code, 201)

        getting_lead = json.loads(response.body)

        self.assertIn('name', getting_lead)
        self.assertEqual(getting_lead['name'], 'Test User')
        self.assertEqual(getting_lead["first_name"], "Test")
        self.assertEqual(getting_lead["phone"], "+15551234567")
        self.assertEqual(getting_lead["email"], "test@example.com")
        self.assertEqual(getting_lead["adv_id"], 1)

    async def test_update_lead(self):
        payload = {
            "name": "Test User",
            "first_name": "Test",
            "phone": "+15551234567",
            "email": "test@example.com",
            "adv_id": 1,
        }
        updated_payload = {
            "name": "Updated Test User",
            "first_name": "UpdatedTest",
            "phone": "+15557654321",
            "email": "updated_test@example.com",
            "adv_id": 33,
        }
        response = await self.async_fetch('/leads', method="POST", body=json.dumps(payload),
                                          headers={'Content-Type': 'application/json'})
        self.assertEqual(response.code, 201)

        lead = json.loads(response.body)
        created_lead = await self.async_fetch(f'/leads/{lead['id']}')
        self.assertEqual(created_lead.code, 201)

        created_lead = json.loads(response.body)

        updated_lead = await self.async_fetch(f'/leads/{created_lead['id']}', method="PUT", body=json.dumps(updated_payload),
                                          headers={'Content-Type': 'application/json'})
        self.assertEqual(response.code, 201)

        updated_lead = json.loads(updated_lead.body)


        self.assertIn('name', updated_lead)
        self.assertEqual(updated_lead['name'], 'Updated Test User')
        self.assertEqual(updated_lead["first_name"], "UpdatedTest")
        self.assertEqual(updated_lead["phone"], "+15557654321")
        self.assertEqual(updated_lead["email"], "updated_test@example.com")
        self.assertEqual(updated_lead["adv_id"], 33)

    async def test_delete_lead(self):
        payload = {
            "name": "Test User",
            "first_name": "Test",
            "phone": "+15551234567",
            "email": "test@example.com",
            "adv_id": 1,
        }

        response = await self.async_fetch('/leads', method="POST", body=json.dumps(payload),
                                          headers={'Content-Type': 'application/json'})
        self.assertEqual(response.code, 201)

        lead = json.loads(response.body)
        created_lead = await self.async_fetch(f'/leads/{lead['id']}')
        self.assertEqual(created_lead.code, 201)

        deleted_lead = await self.async_fetch(f'/leads/{lead['id']}', method="DELETE")

        self.assertEqual(deleted_lead.code, 204)

        deleted_lead = await self.async_fetch(f'/leads/{deleted_lead['id']}')

        self.assertEqual(deleted_lead.code, 404)


