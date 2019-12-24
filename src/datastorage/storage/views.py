from rest_framework import mixins
from rest_framework import exceptions
from rest_framework.generics import get_object_or_404

from utils.viewsets import JSONSchemaViewSet


class GetOrRetrieveMixin:
    
    def list_or_retrieve(self, request, *args, **kwargs):
        if self.kwargs["storage_pk"]:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)


class StorageViewSet(mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin,
                     GetOrRetrieveMixin,
                     JSONSchemaViewSet):
    lookup_field = 'storage_key'
    lookup_url_kwarg = 'storage_key'
    lookup_value_regex = r'[0-9A-Za-z-_/]+'
    
    def initialize_request(self, request, *args, **kwargs):
        from factory.storage.model_factory import Storage
        from factory.models import Storage as FactoryStorage
        try:
            storage_attrs = self.kwargs[self.lookup_url_kwarg].split('/')
            if len(storage_attrs) == 1:
                storage_name, storage_pk = storage_attrs[0], None
            else:
                storage_name, storage_pk = storage_attrs

            self.kwargs["storage"] = FactoryStorage.objects.last_versions().get(name=storage_name)
            self.kwargs["storage_model"] = Storage(self.kwargs['storage'], 'storage.models')
            self.kwargs["storage_pk"] = storage_pk
            return super().initialize_request(request)
        except (ValueError, KeyError, FactoryStorage.DoesNotExist):
            raise exceptions.NotFound()
    
    def get_serializer_class(self):
        from rest_framework.serializers import ModelSerializer
        
        class StorageSerializer(ModelSerializer):
            class Meta:
                model = self.kwargs["storage_model"]
                fields = ["keyfield", "version", "created_at", "updated_at", "sf2"]
        return StorageSerializer

    def get_queryset(self):
        from factory.storage.model_factory import Storage
        return self.kwargs["storage_model"].objects
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return get_object_or_404(queryset, keyfield=self.kwargs["storage_pk"])

    def get_json_schema(self):
        # TODO: based on self.kwargs['storage']
        class JsonSchema:
            json = {
                "type": "object"
            }
        return JsonSchema

