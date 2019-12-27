import json

from django.test import TestCase
from django.test import Client


class StorageAPITestCase(TestCase):
    
    def is_field_in_details(self, field, content):
        return field in json.loads(content)['detail']
    
    def create_storage_foo(self):
        c = Client()
        r = c.post(
            "/api/v1/factory/storage/",
            content_type="application/json",
            data={
                "name": "Foo",
                "key": {"name": "id", "type": "string", "max_length": 5},
                "fields": [
                    {"name": "fieldstring", "max_length": 32, "type": "string", "db_index": True},
                    {"name": "fieldint", "type": "integer", "db_index": True},
                    {"name": "fieldstring2", "max_length": 16, "type": "string"},
                    {"name": "fieldtext", "type": "text"}
                ]
            }
        )
    
    def update_storage_foo(self):
        c = Client()
        r = c.post(
            "/api/v1/factory/storage/",
            content_type="application/json",
            data={
                "name": "Foo",
                "key": {"name": "id", "type": "string", "max_length": 5},
                "fields": [
                    {"name": "fieldstring", "max_length": 32, "type": "string", "db_index": True},
                    {"name": "fieldint", "type": "integer", "db_index": True},
                    {"name": "fieldstring2", "max_length": 16, "type": "string"},
                    {"name": "fieldtext", "type": "text"},
                    {"name": "fieldint2", "type": "integer", "db_index": True, "default": 1},
                    {"name": "fieldlong", "type": "long", "db_index": True, "default": 2},
                    {"name": "fieldstring3", "max_length": 16, "type": "string", "default": "S", "db_index": True},
                    {"name": "fieldtext2", "type": "text", "default": "T"}
                ]
            }
        )
    
    def test_url_validation(self):
        c = Client()
        
        # Send empty data
        r = c.get('/api/v1/storage/foo1/')
        self.assertEqual(r.status_code, 404)

        r = c.get('/api/v1/storage/foo1/1/')
        self.assertEqual(r.status_code, 404)

        r = c.get('/api/v1/storage/foo1/1/1')
        self.assertEqual(r.status_code, 404)
    
    def test_positive_flow(self):
        # TODO: add list filters
        self.create_storage_foo()
        c = Client()
        r = c.get('/api/v1/storage/Foo/')
        self.assertEqual(r.status_code, 200)
        
        r = c.post(
            '/api/v1/storage/Foo/',
            content_type="application/json",
            data={
                "id": "foo1",
                "fieldstring": "f1",
                "fieldint": 2,
                "fieldstring2": "fs3",
                "fieldtext": "SELECT * from factory_storage"
            }
        )
        self.assertEqual(r.status_code, 201)
        content = json.loads(r.content)
        self.assertTrue('id' in content)
        self.assertTrue('fieldstring' in content)
        self.assertTrue('fieldint' in content)
        self.assertTrue('fieldstring2' in content)
        self.assertTrue('fieldtext' in content)
        self.assertTrue('version' in content)
        self.assertTrue('created_at' in content)
        self.assertTrue('updated_at' in content)
        
        r = c.get('/api/v1/storage/Foo/foo1/')
        self.assertEqual(r.status_code, 200)
        got_content = json.loads(r.content)
        self.assertEqual(got_content['id'], content['id'])
        self.assertEqual(got_content['fieldstring'], content['fieldstring'])
        self.assertEqual(got_content['fieldint'], content['fieldint'])
        self.assertEqual(got_content['fieldstring2'], content['fieldstring2'])
        self.assertEqual(got_content['fieldtext'], content['fieldtext'])
        self.assertEqual(got_content['version'], content['version'])
        self.assertEqual(got_content['created_at'], content['created_at'])
        self.assertEqual(got_content['updated_at'], content['updated_at'])
        
        self.update_storage_foo()
        r = c.get('/api/v1/storage/Foo/foo1/')
        self.assertEqual(r.status_code, 200)
        got_content = json.loads(r.content)
        self.assertEqual(got_content['id'], content['id'])
        self.assertEqual(got_content['fieldstring'], content['fieldstring'])
        self.assertEqual(got_content['fieldint'], content['fieldint'])
        self.assertEqual(got_content['fieldstring2'], content['fieldstring2'])
        self.assertEqual(got_content['fieldtext'], content['fieldtext'])
        self.assertEqual(got_content['fieldint2'], 1)
        self.assertEqual(got_content['fieldlong'], 2)
        self.assertEqual(got_content['fieldstring3'], "S")
        self.assertEqual(got_content['fieldtext2'], "T")
        self.assertEqual(got_content['version'], content['version'])
        self.assertEqual(got_content['created_at'], content['created_at'])
        self.assertEqual(got_content['updated_at'], content['updated_at'])
