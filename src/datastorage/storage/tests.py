import json

from django.test import TestCase
from django.test import Client


class StorageAPITestCase(TestCase):
    
    def is_field_in_details(self, field, content):
        return field in json.loads(content)['detail']
    
    def test_url_validation(self):
        c = Client()
        
        # Send empty data
        r = c.get('/api/v1/storage/foo1/')
        self.assertEqual(r.status_code, 404)

        r = c.get('/api/v1/storage/foo1/1/')
        self.assertEqual(r.status_code, 404)

        r = c.get('/api/v1/storage/foo1/1/1')
        self.assertEqual(r.status_code, 404)