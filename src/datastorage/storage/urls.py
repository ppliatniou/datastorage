from rest_framework import routers

from storage import views


class StorageRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'list_or_retrieve',
                'post': 'create',
                'put': 'update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        routers.DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]

router = StorageRouter()

router.register(r'v1/storage', views.StorageViewSet, basename='v1_storage')

urlpatterns = router.urls
