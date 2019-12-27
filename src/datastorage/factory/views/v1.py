from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from utils.viewsets import JSONSchemaViewSet
from utils.pagination import StandardResultsSetPagination
from utils.exceptions import ConflictError

from factory.views import schemas
from factory.views.serializers import StorageSerializer, MigrationSerializer
from factory.models import Storage, StorageMigration
from factory.storage.validation import is_valid as is_storage_valid
from factory.storage.compatibility import is_compatible as is_storage_compatible
from factory.storage.migration import create_migration_diff
from factory.tasks import perform_migration


class StorageFactoryViewSet(JSONSchemaViewSet):
    json_schema = schemas.v1_create_storage
    queryset = Storage.objects.last_versions().order_by('-created_at')
    serializer_class = StorageSerializer
    lookup_field = 'name'
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        data = request.data
        storage_definition = {
            'key': data['key'],
            'fields': data['fields']
        }

        is_storage_valid(storage_definition)
        
        storage_name = data['name']
        qs = self.get_queryset()
        previous = None
        try:
            previous = qs.get(name=storage_name)
            if previous.locked:
                raise ConflictError(detail="Last version of storage is still locked")

            is_storage_compatible(previous.definition, storage_definition)

            data = {
                "name": storage_name,
                "version": previous.version + 1,
                "definition": storage_definition
            }
            previous.last_version = False
            previous.save()
        except Storage.DoesNotExist:
            data = {
                "name": storage_name,
                "version": 1,
                "definition": storage_definition
            }
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = serializer.instance
        migration_diff = create_migration_diff(previous, instance)
        sm = StorageMigration.objects.create(
            name=instance.name,
            version=instance.version,
            definition=migration_diff
        )
        perform_migration.delay(sm.id)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReadyStatusViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Storage.objects.last_versions()
    serializer_class = MigrationSerializer
    lookup_field = 'name'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        migration = StorageMigration.objects.get(name=instance.name, version=instance.version)
        
        serializer = self.get_serializer(migration)
        return Response(serializer.data)


