from collections import namedtuple

from utils.registry import BaseRegistry
from utils import exceptions

from factory.models import Storage as FactoryStorage
from factory.storage.model_factory import Storage

from storage.serializer_factory import Serializer
from storage.filter_factory import ModelFilter


__all__ = (
    'registry',
)

StorageMeta = namedtuple(
    'StorageMeta',
    ['name', 'pk_field', 'fields', 'serializer_class', 'filterset_class']
)


class ModelRegistry(BaseRegistry):
    
    def register(self, name):
        try:
            fstorage = FactoryStorage.objects.last_versions().get(name=name)
            if fstorage.locked:
                raise exceptions.LockedStorageError('Storage is temporary unavailable')
            model = Storage(fstorage, 'storage.models')
            self.registry[name] = model
            self.registry[name].storage_meta = StorageMeta(
                name=name,
                pk_field=fstorage.definition["key"]["name"],
                fields=[f["name"] for f in fstorage.definition["fields"]],
                serializer_class=Serializer(fstorage, model),
                filterset_class=ModelFilter(fstorage, model)
            )
        except FactoryStorage.DoesNotExist:
            raise exceptions.RegistryError("Storage doesn't exist")
    
    def get(self, name):
        if 'name' not in self.registry:
            self.register(name)
        return self.registry[name]
    
    def remove(self, name):
        if 'name' in self.registry:
            del self.registry['name']


registry = ModelRegistry()