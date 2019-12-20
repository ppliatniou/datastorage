from rest_framework.serializers import ModelSerializer

from factory.models import Factory


class FactorySerializer(ModelSerializer):
    
    class Meta:
        model = Factory
        fields = []
