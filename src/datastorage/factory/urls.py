from rest_framework import routers

from factory.views import v1

router = routers.SimpleRouter()

router.register(r'v1/factory/storage', v1.StorageFactoryViewSet, basename='v1_factory')
router.register(r'v1/factory/ready_status', v1.ReadyStatusViewSet, basename='v1_factory_ready_status')

urlpatterns = router.urls
