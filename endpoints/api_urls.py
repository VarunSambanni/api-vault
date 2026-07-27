from rest_framework.routers import DefaultRouter
from .api_views import APIEndpointViewSet

app_name = "api"

router = DefaultRouter()
router.register("endpoints", APIEndpointViewSet, basename="endpoint")

urlpatterns = router.urls