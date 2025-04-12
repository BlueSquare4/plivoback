# status/serializers.py
from rest_framework import serializers
from .models import Service, Incident, Maintenance

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ['id', 'service', 'title', 'description', 'is_resolved', 'created_at']
        read_only_fields = ['id', 'created_at']

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ['id', 'service', 'title', 'description', 'scheduled_start', 'scheduled_end', 'is_completed', 'created_at']
        read_only_fields = ['id', 'created_at']
