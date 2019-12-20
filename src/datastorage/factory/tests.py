import json

from django.test import TestCase
from django.test import Client


class FactoryAPITestCase(TestCase):
    
    def is_field_in_details(self, field, content):
        return field in json.loads(content)['detail']
    
    def test_negative_validation(self):
        c = Client()
        
        # Send empty data
        r = c.post('/api/v1/factory/', {}, content_type='application/json')
        self.assertEqual(r.status_code, 400)
        self.assertTrue(self.is_field_in_details('name', r.content))
        # Send only name
        r = c.post('/api/v1/factory/', {"name": "storage"}, content_type='application/json')
        self.assertEqual(r.status_code, 400)
        self.assertTrue(self.is_field_in_details('key', r.content))
        # Send name and key
        r = c.post(
            '/api/v1/factory/',
            {"name": "storage", "key": {"name": "id", "type": "integer"}},
            content_type='application/json'
        )
        self.assertEqual(r.status_code, 400)
        self.assertTrue(self.is_field_in_details('fields', r.content))
        # Send empty fields
        r = c.post(
            '/api/v1/factory/',
            {
                "name": "storage",
                "key": {"name": "id", "type": "integer"},
                "fields": [],
            },
            content_type='application/json'
        )
        self.assertEqual(r.status_code, 400)
        self.assertTrue(self.is_field_in_details('[]', r.content))
        # Send wrong key
        r = c.post(
            '/api/v1/factory/',
            {
                "name": "storage",
                "key": {"name": "id", "type": "text"},
                "fields": [{"name": "sfield", "type": "long"}],
            },
            content_type='application/json'
        )
        self.assertEqual(r.status_code, 400)
        self.assertTrue(self.is_field_in_details('text', r.content))
        # Send empty indexes
        r = c.post(
            '/api/v1/factory/',
            {
                "name": "storage",
                "key": {"name": "id", "type": "integer"},
                "fields": [{"name": "sfield", "type": "long"}],
                "indexes": {"unique": []}
            },
            content_type='application/json'
        )
        self.assertEqual(r.status_code, 400)
        self.assertTrue(self.is_field_in_details('[]', r.content))
