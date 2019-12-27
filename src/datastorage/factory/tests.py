import json

from django.test import TestCase
from django.test import Client
from django.db import connection

from factory.storage.validation import RESERVED_NAMES


class FactoryAPITestCase(TestCase):
    
    def is_field_in_details(self, field, content):
        return field in json.loads(content)['detail']
    
    def test_negative_data_validation(self):
        c = Client()
        
        # Send empty data
        r = c.post('/api/v1/factory/storage/', {}, content_type='application/json')
        self.assertEqual(r.status_code, 400)
        self.assertTrue(self.is_field_in_details('name', r.content))
        # Send only name
        r = c.post('/api/v1/factory/storage/', {"name": "storage"}, content_type='application/json')
        self.assertEqual(r.status_code, 400)
        self.assertTrue(self.is_field_in_details('key', r.content))
        # Send name and key
        r = c.post(
            '/api/v1/factory/storage/',
            {"name": "storage", "key": {"name": "id", "type": "integer"}},
            content_type='application/json'
        )
        self.assertEqual(r.status_code, 400)
        self.assertTrue(self.is_field_in_details('fields', r.content))
        # Send empty fields
        r = c.post(
            '/api/v1/factory/storage/',
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
            '/api/v1/factory/storage/',
            {
                "name": "storage",
                "key": {"name": "id", "type": "text"},
                "fields": [{"name": "sfield", "type": "long"}],
            },
            content_type='application/json'
        )
        self.assertEqual(r.status_code, 400)
        self.assertTrue(self.is_field_in_details('text', r.content))
        # Testing reserved names
        for rname in RESERVED_NAMES:
            r = c.post(
                '/api/v1/factory/storage/',
                {
                    "name": "storage",
                    "key": {"name": rname, "type": "integer"},
                    "fields": [{"name": "sfield", "type": "long"}],
                },
                content_type='application/json'
            )
            self.assertEqual(r.status_code, 400)
            r = c.post(
                '/api/v1/factory/storage/',
                {
                    "name": "storage",
                    "key": {"name": "id", "type": "integer"},
                    "fields": [{"name": rname, "type": "long"}],
                },
                content_type='application/json'
            )
            print(r.content)
            self.assertEqual(r.status_code, 400)
            
    
    def test_negative_view_validation(self):
        c = Client()
        
        # Conflict key
        r = c.post(
            '/api/v1/factory/storage/',
            {
                "name": "storage",
                "key": {"name": "id", "type": "integer"},
                "fields": [{"name": "id", "type": "long"}],
            },
            content_type='application/json'
        )
        self.assertEqual(r.status_code, 400)
        self.assertTrue(self.is_field_in_details('id', r.content))
        
    def test_storage_creation(self):
        c = Client()
        key = {"name": "id", "type": "integer"}
        fields = [{"name": "sfield", "type": "long"}]
        data = {
            "name": "storage",
            "key": key,
            "fields": fields
        }
        r = c.post(
            "/api/v1/factory/storage/",
            data,
            content_type="application/json"
        )
        self.assertEqual(r.status_code, 201)
        content = json.loads(r.content)
        self.assertEqual(content["name"], "storage")
        self.assertEqual(content["version"], 1)
        self.assertTrue(content["locked"])
        self.assertEqual(
            content["definition"],
            {
                "key": key,
                "fields": fields
            }
        )
        
        r = c.get('/api/v1/factory/storage/storage/')
        content = json.loads(r.content)
        self.assertEqual(content["name"], "storage")
        self.assertEqual(content["version"], 1)
        self.assertFalse(content["locked"])
        self.assertEqual(
            content["definition"],
            {
                "key": key,
                "fields": fields
            }
        )

        r = c.get('/api/v1/factory/ready_status/storage/')
        content = json.loads(r.content)
        self.assertEqual(content["name"], "storage")
        self.assertEqual(content["version"], 1)
        self.assertTrue(content["applied"])

    def test_storage_update(self):
        c = Client()
        key = {"name": "id", "type": "integer"}
        fields = [{"name": "sfield", "type": "long"}]
        data = {
            "name": "storage",
            "key": key,
            "fields": fields
        }
        r = c.post(
            "/api/v1/factory/storage/",
            data,
            content_type="application/json"
        )
        self.assertEqual(r.status_code, 201)
        content = json.loads(r.content)
        self.assertEqual(content["name"], "storage")
        self.assertEqual(content["version"], 1)
        self.assertTrue(content["locked"])
        self.assertEqual(
            content["definition"],
            {
                "key": key,
                "fields": fields
            }
        )

        fields = [
            {"name": "sfield", "type": "long"},
            {"name": "sfield2", "type": "string", "max_length": 16, "default": ""}
        ]
        data = {
            "name": "storage",
            "key": key,
            "fields": fields
        }
        r = c.post(
            "/api/v1/factory/storage/",
            data,
            content_type="application/json"
        )
        self.assertEqual(r.status_code, 201)
        content = json.loads(r.content)
        self.assertEqual(content["name"], "storage")
        self.assertEqual(content["version"], 2)
        self.assertTrue(content["locked"])
        self.assertEqual(
            content["definition"],
            {
                "key": key,
                "fields": fields
            }
        )
    
        r = c.get('/api/v1/factory/storage/storage/')
        content = json.loads(r.content)
        self.assertEqual(content["name"], "storage")
        self.assertEqual(content["version"], 2)
        self.assertFalse(content["locked"])
        self.assertEqual(
            content["definition"],
            {
                "key": key,
                "fields": fields
            }
        )

    def test_storage_compatibility(self):
        c = Client()
        key = {"name": "id", "type": "integer"}
        fields = [
            {"name": "sfield", "type": "long"},
            {"name": "sfield2", "type": "integer"}
        ]
        data = {
            "name": "storage",
            "key": key,
            "fields": fields
        }
        r = c.post(
            "/api/v1/factory/storage/",
            data,
            content_type="application/json"
        )
        self.assertEqual(r.status_code, 201)
        content = json.loads(r.content)
        self.assertEqual(content["name"], "storage")
        self.assertEqual(content["version"], 1)
        self.assertTrue(content["locked"])
        self.assertEqual(
            content["definition"],
            {
                "key": key,
                "fields": fields
            }
        )
        
        # Key conflict
        fields = [
            {"name": "sfield", "type": "long"},
            {"name": "sfield2", "type": "string", "max_length": 16, "default": ""}
        ]
        data = {
            "name": "storage",
            "key": {"name": "maxv", "type": "integer"},
            "fields": fields
        }
        r = c.post(
            "/api/v1/factory/storage/",
            data,
            content_type="application/json"
        )
        self.assertEqual(r.status_code, 400)
        self.assertTrue(self.is_field_in_details('Key', r.content))
        
        # Removed fields
        fields = [
            {"name": "sfield", "type": "long"}
        ]
        data = {
            "name": "storage",
            "key": key,
            "fields": fields
        }
        r = c.post(
            "/api/v1/factory/storage/",
            data,
            content_type="application/json"
        )
        self.assertEqual(r.status_code, 400)
        self.assertTrue(self.is_field_in_details('sfield2', r.content))

        # Different definitions fields
        fields = [
            {"name": "sfield", "type": "long"},
            {"name": "sfield2", "type": "long"}
        ]
        data = {
            "name": "storage",
            "key": key,
            "fields": fields
        }
        r = c.post(
            "/api/v1/factory/storage/",
            data,
            content_type="application/json"
        )
        self.assertEqual(r.status_code, 400)
        self.assertTrue(self.is_field_in_details('sfield2', r.content))

        # No default value
        fields = [
            {"name": "sfield", "type": "long"},
            {"name": "sfield2", "type": "integer"},
            {"name": "sfield3", "type": "integer"}
        ]
        data = {
            "name": "storage",
            "key": key,
            "fields": fields
        }
        r = c.post(
            "/api/v1/factory/storage/",
            data,
            content_type="application/json"
        )
        self.assertEqual(r.status_code, 400)
        self.assertTrue(self.is_field_in_details('sfield3', r.content))
    
    def test_creation_all_fields(self):
        c = Client()
        key = {"name": "idkey", "type": "integer"}
        fields = [
            {"name": "fieldlong", "type": "long", "db_index": True},
            {"name": "fieldint", "type": "integer", "db_index": True},
            {"name": "fieldstring", "type": "string", "max_length": 64, "db_index": True},
            {"name": "fieldtext", "type": "text"},
            
        ]
        data = {
            "name": "storage",
            "key": key,
            "fields": fields
        }
        r = c.post(
            "/api/v1/factory/storage/",
            data,
            content_type="application/json"
        )
        self.assertEqual(r.status_code, 201)
        content = json.loads(r.content)
        self.assertEqual(content["name"], "storage")
        self.assertEqual(content["version"], 1)
        self.assertTrue(content["locked"])
        self.assertEqual(
            content["definition"],
            {
                "key": key,
                "fields": fields
            }
        )
        cursor = connection.cursor()
        sql_res = cursor.execute(
            "SELECT column_name, is_nullable, data_type, character_maximum_length "
            "FROM information_schema.COLUMNS "
            "WHERE TABLE_NAME = 'storage_storage'"
        )
        res = cursor.fetchall()
        self.assertTrue(("idkey", 'NO', 'integer', None) in res)
        self.assertTrue(("fieldint", 'NO', 'integer', None) in res)
        self.assertTrue(("fieldlong", 'NO', 'bigint', None) in res)
        self.assertTrue(("fieldstring", 'NO', 'character varying', 64) in res)
        self.assertTrue(("fieldtext", 'NO', 'text', None) in res)
        # Service fields
        self.assertTrue(("version", 'NO', 'integer', None) in res)
        self.assertTrue(("created_at", 'NO', 'timestamp with time zone', None) in res)
        self.assertTrue(("updated_at", 'NO', 'timestamp with time zone', None) in res)

    def test_update_all_fields_with_default_value(self):
        c = Client()
        key = {"name": "idkey", "type": "integer"}
        fields = [
            {"name": "fieldtext", "type": "text"},
        ]
        data = {
            "name": "storage",
            "key": key,
            "fields": fields
        }
        r = c.post(
            "/api/v1/factory/storage/",
            data,
            content_type="application/json"
        )
        self.assertEqual(r.status_code, 201)
        content = json.loads(r.content)
        self.assertEqual(content["name"], "storage")
        self.assertEqual(content["version"], 1)
        self.assertTrue(content["locked"])
        self.assertEqual(
            content["definition"],
            {
                "key": key,
                "fields": fields
            }
        )
        cursor = connection.cursor()
        sql_res = cursor.execute(
            "SELECT column_name, is_nullable, data_type, character_maximum_length "
            "FROM information_schema.COLUMNS "
            "WHERE TABLE_NAME = 'storage_storage'"
        )
        res = cursor.fetchall()
        self.assertTrue(("idkey", 'NO', 'integer', None) in res)
        self.assertTrue(("fieldtext", 'NO', 'text', None) in res)
        # Service fields
        self.assertTrue(("version", 'NO', 'integer', None) in res)
        self.assertTrue(("created_at", 'NO', 'timestamp with time zone', None) in res)
        self.assertTrue(("updated_at", 'NO', 'timestamp with time zone', None) in res)

        fields = [
            {"name": "fieldtext", "type": "text"},
            {"name": "fieldlong1", "type": "long", "db_index": True, "default": 1200},
            {"name": "fieldint1", "type": "integer", "db_index": True, "default": 12},
            {"name": "fieldstring1", "type": "string", "max_length": 64, "db_index": True, "default": "abc"},
            {"name": "fieldtext1", "type": "text", "default": "text"},
        ]
        
        data = {
            "name": "storage",
            "key": key,
            "fields": fields
        }
        r = c.post(
            "/api/v1/factory/storage/",
            data,
            content_type="application/json"
        )
        self.assertEqual(r.status_code, 201)
        content = json.loads(r.content)
        self.assertEqual(content["name"], "storage")
        self.assertEqual(content["version"], 2)
        self.assertTrue(content["locked"])
        self.assertEqual(
            content["definition"],
            {
                "key": key,
                "fields": fields
            }
        )
        cursor = connection.cursor()
        sql_res = cursor.execute(
            "SELECT column_name, is_nullable, data_type, character_maximum_length, column_default "
            "FROM information_schema.COLUMNS "
            "WHERE TABLE_NAME = 'storage_storage'"
        )
        res = cursor.fetchall()
        self.assertTrue(("idkey", 'NO', 'integer', None, None) in res)
        self.assertTrue(("fieldtext", 'NO', 'text', None, None) in res)
        self.assertTrue(("fieldint1", 'NO', 'integer', None, "12") in res)
        self.assertTrue(("fieldlong1", 'NO', 'bigint', None, "1200") in res)
        self.assertTrue(("fieldstring1", 'NO', 'character varying', 64, "'abc'::character varying") in res)
        self.assertTrue(("fieldtext1", 'NO', 'text', None, "'text'::text") in res)
        # Service fields
        self.assertTrue(("version", 'NO', 'integer', None, None) in res)
        self.assertTrue(("created_at", 'NO', 'timestamp with time zone', None, None) in res)
        self.assertTrue(("updated_at", 'NO', 'timestamp with time zone', None, None) in res)
