from django.urls import path, include
from rest_framework.routers import DefaultRouter
from status.views import ServiceViewSet, IncidentViewSet, MaintenanceViewSet, test_notify
from django.contrib import admin

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'incidents', IncidentViewSet)
router.register(r'maintenances', MaintenanceViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # ✅ everything under /api/
    path('test-notify/', test_notify, name="test_notify"),
]
