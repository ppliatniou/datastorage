from rest_framework.response import Response
from rest_framework import status

from utils.viewsets import JSONSchemaViewSet

from factory.views import schemas
from factory.views.serializers import FactorySerializer
from factory.models import Storage


class FactoryViewSet(JSONSchemaViewSet):
    json_schema = schemas.v1_create_storage
    queryset = Storage.objects.last_versions().order_by('-created_at')
    serializer_class = FactorySerializer
    lookup_field = 'name'

    def create(self, request, *args, **kwargs):
        data = request.data
        storage_name = data['name']
        qs = self.get_queryset()
        try:
            s = qs.get(name=storage_name)

            data = {
                "name": storage_name,
                "version": s.version + 1,
                "definition": {
                    'key': data['key'],
                    'fields': data['fields'],
                    'indexes': data.get('indexes', {})
                }
            }
        except Storage.DoesNotExist:
            data = {
                "name": storage_name,
                "version": 1,
                "definition": {
                    'key': data['key'],
                    'fields': data['fields'],
                    'indexes': data.get('indexes', {})
                }
            }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


