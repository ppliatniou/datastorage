from rest_framework.serializers import ModelSerializer

from factory.models import Storage, StorageMigration

__all__ = (
    'StorageSerializer',
    'MigrationSerializer',
)


class StorageSerializer(ModelSerializer):
    
    class Meta:
        model = Storage
        fields = ["name", "version", "locked", "definition", "created_at", "updated_at"]


class MigrationSerializer(ModelSerializer):
    
    class Meta:
        model = StorageMigration
        fields = ["name", "version", "applied"]
