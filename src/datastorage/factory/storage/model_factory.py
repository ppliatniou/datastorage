from django.db import models

from factory.models import Storage as StorageDefinition
from factory.storage.registry import field_registry


__all__ = (
    'Storage',
)


def Storage(storage, module='factory.models'):
    class_attrs = {}
    class_attrs['__module__'] = module
    class_attrs["version"] = models.IntegerField(default=1)
    class_attrs["created_at"] = models.DateTimeField(auto_now_add=True)
    class_attrs["updated_at"] = models.DateTimeField(auto_now=True)

    key_definition = storage.definition["key"]
    key_field = field_registry.get(key_definition["type"])
    class_attrs[key_definition["name"]] = key_field.django_db_field(key_definition, is_pk=True)

    for field_def in storage.definition["fields"]:
        field = field_registry.get(field_def["type"])
        class_attrs[field_def["name"]] = field.django_db_field(field_def)

    StorageModel = type(
        storage.name.lower().capitalize(),
        (models.Model,),
        class_attrs
    )
            
    return StorageModel
