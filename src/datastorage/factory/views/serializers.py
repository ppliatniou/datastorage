from rest_framework.serializers import ModelSerializer

from factory.models import Storage


class FactorySerializer(ModelSerializer):
    
    class Meta:
        model = Storage
        fields = ["name", "version", "locked", "definition", "created_at", "updated_at"]
