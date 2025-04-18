# status/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# from rest_framework.authentication import TokenAuthentication  # or your FirebaseAuthentication
from .authentication import FirebaseAuthentication
from .models import Service, Incident, Maintenance
from .serializers import ServiceSerializer, IncidentSerializer, MaintenanceSerializer
from .utils import notify_clients
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotAllowed
import os
import json
from django.http import JsonResponse
import base64
from dotenv import load_dotenv

load_dotenv()


def test_env(request):
    firebase_b64 = os.environ.get("FIREBASE_CREDENTIAL_BASE64")
    if not firebase_b64:
       raise Exception("Missing FIREBASE_CREDENTIAL_BASE64 environment variable")
    try:
       firebase_json = json.loads(base64.b64decode(firebase_b64).decode("utf-8"))
    except Exception as e:
       raise Exception(f"Invalid Firebase credential JSON: {e}")
    
    return JsonResponse({"firebase": firebase_json})


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        svc = serializer.save(user=self.request.user)
        notify_clients(
            {
                "type": "instance",
                "action": "created",
                "data": ServiceSerializer(svc).data,
            }
        )


class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # only incidents on this user's services
        return self.queryset.filter(service__user=self.request.user)

    def perform_create(self, serializer):
        incident = serializer.save()
        notify_clients(
            {
                "type": "incident",
                "action": "created",
                "data": IncidentSerializer(incident).data,
            }
        )

    def perform_update(self, serializer):
        incident = serializer.save()
        notify_clients(
            {
                "type": "incident",
                "action": "updated",
                "data": IncidentSerializer(incident).data,
            }
        )

    def perform_destroy(self, instance):
        notify_clients(
            {
                "type": "incident",
                "action": "deleted",
                "data": IncidentSerializer(instance).data,
            }
        )
        instance.delete()


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(service__user=self.request.user)

    def perform_create(self, serializer):
        m = serializer.save()
        notify_clients(
            {
                "type": "maintenance",
                "action": "scheduled",
                "data": MaintenanceSerializer(m).data,
            }
        )

    def perform_update(self, serializer):
        m = serializer.save()
        notify_clients(
            {
                "type": "maintenance",
                "action": "completed" if m.is_completed else "updated",
                "data": MaintenanceSerializer(m).data,
            }
        )


# # catch‑all notifier
# notify_clients({"message": "Service status updated!"})

# @csrf_exempt
# def test_notify(request):
#     if request.method != "POST":
#         return HttpResponseNotAllowed(["POST"])
#     try:
#         payload = json.loads(request.body)
#     except json.JSONDecodeError:
#         return JsonResponse({"error": "Invalid JSON"}, status=400)
#     notify_clients(payload)
#     return JsonResponse({"status": "ok", "sent": payload})
