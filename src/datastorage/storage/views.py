from rest_framework.viewsets import ModelViewSet
from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from django.db import transaction, IntegrityError

from utils import exceptions as app_exceptions

from storage.model_registry import registry as model_registry


class GetOrRetrieveMixin:
    
    def list_or_retrieve(self, request, *args, **kwargs):
        if self.kwargs["storage_pk"]:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)


class StorageViewSet(GetOrRetrieveMixin,
                     ModelViewSet):
    lookup_field = 'storage_key'
    lookup_url_kwarg = 'storage_key'
    lookup_value_regex = r'[0-9A-Za-z-_/]+'
    
    def get_storage_model(self):
        return self.kwargs["storage"]
    
    def get_storage_pk(self):
        return self.kwargs["storage_pk"]
    
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            self.headers = self.default_response_headers
            response = self.handle_exception(e)
            self.response = self.finalize_response(
                Request(
                    request
                ),
                response, *args, **kwargs)
            return self.response
    
    def initialize_request(self, request, *args, **kwargs):
        try:
            storage_attrs = self.kwargs[self.lookup_url_kwarg].split('/')
            if len(storage_attrs) == 1:
                storage_name, storage_pk = storage_attrs[0], None
            else:
                storage_name, storage_pk = storage_attrs
            self.kwargs["storage"] = model_registry.get(storage_name)
            self.kwargs["storage_pk"] = storage_pk
        except (ValueError, KeyError, app_exceptions.RegistryError):
            raise exceptions.NotFound()
        except app_exceptions.LockedStorageError:
            raise app_exceptions.ConflictError(detail="Storage may temporary unavailable")
        return super().initialize_request(request)
        
    def get_serializer_class(self):
        return self.get_storage_model().storage_meta.serializer_class

    def get_queryset(self):
        return self.get_storage_model().objects
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return get_object_or_404(
            queryset,
            **{self.get_storage_model().storage_meta.pk_field: self.get_storage_pk()}
        )

    def create_or_update(self, request, *args, **kwargs):
        model = self.get_storage_model()
        instance_pk = request.data.get(
            model.storage_meta.pk_field
        )
        try:
            instance = self.get_queryset()\
                .get(**{
                    model.storage_meta.pk_field: instance_pk
            })
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            version = serializer.validated_data.get("version") or instance.version
            try:
                with transaction.atomic():
                    instance = self.get_queryset() \
                        .select_for_update() \
                        .filter(**{
                            "version": version,
                            self.get_storage_model().storage_meta.pk_field: instance_pk
                    })[0]
                    serializer = self.get_serializer(instance, data=request.data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save(version=version + 1)
            except (IntegrityError, IndexError):
                raise app_exceptions.ConflictError(
                    detail="Data wasn't updated. May concurrency request has been performed"
                )
        except self.get_storage_model().DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                with transaction.atomic():
                    serializer.save()
            except IntegrityError:
                raise app_exceptions.ConflictError(
                    detail="Object with key {} already exist".format(instance_pk)
                )
        return serializer.data
    
    def create(self, request, *args, **kwargs):
        data = self.create_or_update(request, *args, **kwargs)
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        data = self.create_or_update(request, *args, **kwargs)
        return Response(data)
    

