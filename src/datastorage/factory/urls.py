from django.urls import path

from factory.views import v1

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'v1/factory', v1.FactoryViewSet, basename='v1_factory')

urlpatterns = router.urls
