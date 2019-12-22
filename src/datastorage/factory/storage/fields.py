from django.db import models


__all__ = (
    'registry',
)


class BaseSchemaField:
    type_name = None
    json_schema = None
    
    def get_json_schema(self):
        if self.json_schema:
            raise ValueError("json_schema can't be None")
        return self.json_schema()
    
    def sql_def(self, definition, *args, **kwargs):
        raise NotImplementedError("Method sql_def() is not implemented")
    
    def index_definition(self, definition):
        return None
    
    def django_db_field(self, definition):
        raise NotImplementedError("Method django_db_field() is not implemented")


class IntegerSchemaField(BaseSchemaField):
    type_name = "integer"
    json_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 2, "maxLength": 128},
            "type": {"type": "string", "enum": ["integer"]},
            "default": {"type": "integer", "minimum": 0}
        },
        "required": ["name", "type"]
    }
    
    def sql_def(self, definition, *args, **kwargs):
        if kwargs.get('is_pk'):
            return "{} integer NOT NULL UNIQUE PRIMARY KEY".format(definition["name"])
        else:
            return "{} integer NOT NULL".format(definition["name"])
    
    def django_db_field(self, definition, *args, **kwargs):
        field_kwargs = {}
        if kwargs.get("is_pk"):
            field_kwargs["primary_key"] = True
        return models.IntegerField(**field_kwargs)


class LongSchemaField(BaseSchemaField):
    type_name = "long"
    json_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 2, "maxLength": 128},
            "type": {"type": "string", "enum": ["integer"]},
            "default": {"type": "integer", "minimum": 0}
        },
        "required": ["name", "type"]
    }
    
    def sql_def(self, definition, *args, **kwargs):
        if kwargs.get('is_pk'):
            return "{} bigint NOT NULL UNIQUE PRIMARY KEY".format(definition["name"])
        else:
            return "{} bigint NOT NULL".format(definition["name"])
    
    def django_db_field(self, definition, *args, **kwargs):
        field_kwargs = {}
        if kwargs.get("is_pk"):
            field_kwargs["primary_key"] = True
        return models.BigIntegerField(**field_kwargs)


class StringSchemaField(BaseSchemaField):
    type_name = "string"
    json_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 2, "maxLength": 128},
            "type": {"type": "string", "enum": ["integer"]},
            "default": {"type": "integer", "minimum": 0}
        },
        "required": ["name", "type"]
    }
    
    def sql_def(self, definition, *args, **kwargs):
        if kwargs.get('is_pk'):
            return "{} character varying({}) UNIQUE PRIMARY KEY".format(
                definition["name"],
                definition["max_length"]
            )
        else:
            return "{} character varying(128) NOT NULL".format(
                definition["name"],
                definition["max_length"]
            )
    
    def django_db_field(self, definition, *args, **kwargs):
        field_kwargs = {
            "max_length": definition["max_length"]
        }
        if kwargs.get("is_pk"):
            field_kwargs["primary_key"] = True
        return models.CharField(**field_kwargs)


class FieldsRegistry:
    
    def __init__(self):
        self.registry = {}
    
    def register(self, field_class):
        self.registry[field_class.type_name] = field_class()
        
    def get_item(self, type_name):
        return self.registry[type_name]


registry = FieldsRegistry()
registry.register(IntegerSchemaField)
registry.register(LongSchemaField)
registry.register(StringSchemaField)