from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from status.views import ServiceViewSet, IncidentViewSet, MaintenanceViewSet, test_notify, test_env

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'incidents', IncidentViewSet)
router.register(r'maintenances', MaintenanceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("test-notify/", test_notify, name="test_notify"),
    path("test-env/", test_env, name="test_env"),  # <-- test endpoint
]
