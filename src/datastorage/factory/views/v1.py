from rest_framework.response import Response

from utils.viewsets import JSONSchemaViewSet

from factory.views import schemas
from factory.models import Factory
from factory.views.serializers import FactorySerializer


class FactoryViewSet(JSONSchemaViewSet):
    json_schema = schemas.v1_create_storage
    queryset = Factory.objects.all()
    serializer_class = FactorySerializer

    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        #
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        #
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)
        return Response({})

    def create(self, request, *args, **kwargs):
        return Response({})
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


