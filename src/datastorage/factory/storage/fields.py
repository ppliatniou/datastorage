from django.db import models

from utils.registry import BaseRegistry


__all__ = (
    'registry',
)


class BaseSchemaField:
    type_name = None
    json_schema = None
    
    def get_json_schema(self):
        if self.json_schema is None:
            raise ValueError("json_schema can't be None")
        return self.json_schema
    
    def sql_def(self, definition, *args, **kwargs):
        """
        :param definition:
        :param args:
        :param kwargs:
        :return: [] - tuples of query statements ADD_COLUMN..., ALTER_COUMN...
            in format ('alter|update', 'statement')
        """
        raise NotImplementedError("Method sql_def() is not implemented")
    
    def index_def(self, definition):
        """
        :param definition:
        :return: bool
        """
        return False
    
    def django_db_field(self, definition):
        """
        :param definition:
        :return: models.Field type definition
        """
        raise NotImplementedError("Method django_db_field() is not implemented")


class IntegerSchemaField(BaseSchemaField):
    type_name = "integer"
    json_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 2, "maxLength": 128},
            "type": {"type": "string", "enum": ["integer"]},
            "db_index": {"type": "boolean", "default": False},
            "default": {"type": "integer", "minimum": 0}
        },
        "additionalProperties": False,
        "required": ["name", "type"]
    }
    
    def sql_def(self, definition, *args, **kwargs):
        statements = []
        if kwargs.get('is_pk'):
            statements.append(
                ("alter", "ADD COLUMN {} integer NOT NULL UNIQUE PRIMARY KEY".format(definition["name"]))
            )
        else:
            statements.append(
                ("alter", "ADD COLUMN {} integer".format(definition["name"]))
            )
            if "default" in definition:
                statements.append(
                    (
                        "alter",
                        "ALTER COLUMN {} SET DEFAULT {}".format(
                            definition["name"],
                            definition["default"]
                        )
                    )
                )
                statements.append(
                    (
                        "update",
                        "SET {}={}".format(
                            definition["name"],
                            definition["default"]
                        )
                    )
                )
            statements.append(
                (
                    "alter",
                    "ALTER COLUMN {} SET NOT NULL".format(definition["name"])
                )
            )
        return statements
    
    def index_def(self, definition):
        return definition.get('db_index', False)
    
    def django_db_field(self, definition, *args, **kwargs):
        field_kwargs = {}
        if kwargs.get("is_pk"):
            field_kwargs["primary_key"] = True
        field_kwargs["default"] = definition.get("default")
        field_kwargs["db_index"] = definition.get("db_index", False)
        return models.IntegerField(**field_kwargs)


class LongSchemaField(BaseSchemaField):
    type_name = "long"
    json_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 2, "maxLength": 128},
            "type": {"type": "string", "enum": ["long"]},
            "db_index": {"type": "boolean", "default": False},
            "default": {"type": "integer", "minimum": 0}
        },
        "additionalProperties": False,
        "required": ["name", "type"]
    }
    
    def sql_def(self, definition, *args, **kwargs):
        statements = []
        if kwargs.get('is_pk'):
            statements.append((
                "alter", "ADD COLUMN {} bigint NOT NULL UNIQUE PRIMARY KEY".format(definition["name"])
            ))
        else:
            statements.append(("alter", "ADD COLUMN {} bigint".format(definition["name"])))
            if "default" in definition:
                statements.append((
                    "alter",
                    "ALTER COLUMN {} SET DEFAULT {}".format(
                        definition["name"],
                        definition["default"]
                    )
                ))
                statements.append(
                    (
                        "update",
                        "SET {}={}".format(
                            definition["name"],
                            definition["default"]
                        )
                    )
                )
            statements.append((
                "alter",
                "ALTER COLUMN {} SET NOT NULL".format(definition["name"])
            ))
        return statements
    
    def index_def(self, definition):
        return definition.get('db_index', False)
    
    def django_db_field(self, definition, *args, **kwargs):
        field_kwargs = {}
        if kwargs.get("is_pk"):
            field_kwargs["primary_key"] = True
        field_kwargs["default"] = definition.get("default")
        field_kwargs["db_index"] = definition.get("db_index", False)
        return models.BigIntegerField(**field_kwargs)


class StringSchemaField(BaseSchemaField):
    type_name = "string"
    
    json_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 2, "maxLength": 128},
            "type": {"type": "string", "enum": ["string"]},
            "max_length": {"type": "integer", "minimum": 1, "maximum": 1024},
            "db_index": {"type": "boolean", "default": False},
            "default": {"type": "string", "minLength": 0}
        },
        "additionalProperties": False,
        "required": ["name", "type", "max_length"]
    }
    
    def sql_def(self, definition, *args, **kwargs):
        statements = []
        if kwargs.get('is_pk'):
            statements.append((
                "alter",
                "ADD COLUMN {} character varying({}) UNIQUE PRIMARY KEY".format(
                    definition["name"],
                    definition["max_length"]
                )
            ))
        else:
            statements.append((
                "alter",
                "ADD COLUMN {} character varying({})".format(
                    definition["name"],
                    definition["max_length"]
                )
            ))
            if "default" in definition:
                statements.append((
                    "alter",
                    "ALTER COLUMN {} SET DEFAULT '{}'".format(
                        definition["name"],
                        definition["default"]
                    )
                ))
                statements.append((
                    "update",
                    "SET {}='{}'".format(
                        definition["name"],
                        definition["default"]
                    )
                ))
            statements.append((
                "alter",
                "ALTER COLUMN {} SET NOT NULL".format(definition["name"])
            ))
        return statements
    
    def index_def(self, definition):
        return definition.get('db_index', False)
    
    def django_db_field(self, definition, *args, **kwargs):
        field_kwargs = {
            "max_length": definition["max_length"]
        }
        if kwargs.get("is_pk"):
            field_kwargs["primary_key"] = True
        field_kwargs["default"] = definition.get("default")
        field_kwargs["db_index"] = definition.get("db_index", False)
        return models.CharField(**field_kwargs)


class TextSchemaField(BaseSchemaField):
    type_name = "text"
    json_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 2, "maxLength": 128},
            "type": {"type": "string", "enum": ["text"]},
            "default": {"type": "string", "minLength": 0}
        },
        "additionalProperties": False,
        "required": ["name", "type"]
    }
    
    def sql_def(self, definition, *args, **kwargs):
        statements = []
        statements.append((
            "alter",
            "ADD COLUMN {} text".format(
                definition["name"]
            )
        ))
        if "default" in definition:
            statements.append((
                "alter",
                "ALTER COLUMN {} SET DEFAULT '{}'".format(
                    definition["name"],
                    definition["default"]
                )
            ))
            statements.append((
                "update",
                "SET {}='{}'".format(
                    definition["name"],
                    definition["default"]
                )
            ))
        statements.append((
            "alter",
            "ALTER COLUMN {} SET NOT NULL".format(
                definition["name"]
            )
        ))
        return statements
    
    def django_db_field(self, definition, *args, **kwargs):
        field_kwargs = {}
        field_kwargs["default"] = definition.get("default")
        field_kwargs["db_index"] = definition.get("db_index", False)
        return models.TextField(**field_kwargs)


class FieldsRegistry(BaseRegistry):
    
    def __init__(self):
        self.registry = {}
    
    def register(self, field_class):
        self.registry[field_class.type_name] = field_class()
        
    def get(self, type_name):
        return self.registry[type_name]


registry = FieldsRegistry()
registry.register(IntegerSchemaField)
registry.register(LongSchemaField)
registry.register(StringSchemaField)
registry.register(TextSchemaField)